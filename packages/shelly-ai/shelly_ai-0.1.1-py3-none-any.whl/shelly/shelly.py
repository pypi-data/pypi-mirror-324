#!/usr/bin/env python3
import asyncio
import fcntl
import os
import pty
import select
import signal
import struct
import subprocess
import sys
import time
import json
import termios
import tty
from collections import deque

from .llm_parser import LLMParser
from .web_socket_error_message_sink import HTTPErrorMessageSink

DEBUG = True


def debug_log(message):
    """Write debug messages to a file instead of stdout"""
    if DEBUG:
        with open('debug.log', 'a') as f:
            f.write(f"{message}\n")


class CircularBuffer:
    def __init__(self, maxlen=2000):
        self.buffer = deque(maxlen=maxlen)
        self.maxlen = maxlen

    def append(self, data):
        lines = data.splitlines(True)

        for line in lines:
            self.buffer.append(line)

    def get_contents(self):
        return ''.join(self.buffer)

    def clear(self):
        self.buffer.clear()


class CommandLogger:
    def __init__(self, maxlines=2000):
        self.current_command = []
        self.current_output = []
        self.last_command = None
        self.stdout_buffer = CircularBuffer(maxlines)
        self.stderr_buffer = CircularBuffer(maxlines)
        self.command_started = False

    def append_to_command(self, data):
        try:
            str_data = data.decode('utf-8')
            for char in str_data:
                if char in ('\r', '\n'):
                    if self.current_command:
                        cmd = ''.join(self.current_command)
                        if cmd.strip():
                            self.last_command = cmd.strip()
                            self.command_started = True
                            self.current_output = []
                        self.current_command = []
                elif char.isprintable():
                    self.current_command.append(char)
                    debug_log(f"Current command: {''.join(self.current_command)}")
        except UnicodeDecodeError:
            pass

    def append_to_output(self, data, stream='stdout'):
        try:
            decoded_data = data.decode('utf-8')
            # Don't include prompt lines in the output
            if not decoded_data.strip().endswith('bash-3.2$'):
                if stream == 'stdout':
                    self.stdout_buffer.append(decoded_data)
                    if self.command_started:
                        self.current_output.append(decoded_data)
                else:
                    self.stderr_buffer.append(decoded_data)
        except UnicodeDecodeError:
            pass

    def get_last_command(self):
        return self.last_command if self.last_command else "No previous command"

    def save_to_file(self, filename='command.log'):
        output_dict = {
            'current_command': ''.join(self.current_command),
            'last_command': self.last_command,
            'current_output': ''.join(self.current_output) if self.current_output else '',
            'buffer': {
                'stdout': self.stdout_buffer.get_contents(),
                'stderr': self.stderr_buffer.get_contents()
            }
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_dict, f, indent=2)


def write_to_file(filename, data):
    with open(filename, 'ab') as f:
        f.write(data)



def analyze_error(sink, parser, cmd_logger):
    cmd_history = {
        'last_command': cmd_logger.get_last_command(),
        'current_output': ''.join(cmd_logger.current_output)
    }

    analysis = asyncio.run(parser.analyze_error(cmd_history))

    error = "Command line execution error. The following error was detected:\n"

    # Handle optional error type and root cause
    error_type = analysis.get('error_type', 'unknown')
    error += f"Error Type: {error_type}\n"

    root_cause = analysis.get('root_cause')
    if root_cause:
        error += f"Root Cause: {root_cause}\n"

    triggering_cmd = analysis.get('triggering_command')
    if triggering_cmd:
        error += f"Command that triggered the error: {triggering_cmd}\n"

    error_messages = analysis.get('error_messages', [])

    if error_messages:
        error += "\nError Messages:\n"
        for err_msg in error_messages:
            if isinstance(err_msg, dict):
                msg = err_msg.get('message')
                if msg:
                    error += f"- {msg}"
                    file_path = err_msg.get('file_path')
                    line_number = err_msg.get('line_number')

                    if file_path:
                        error += f" (in file: {file_path}"
                        if line_number:
                            error += f", line: {line_number}"
                        error += ")"
                    error += "\n"

    affected_files = analysis.get('affected_files', [])
    if affected_files:
        error += "\nAffected files:\n"
        for file in affected_files:
            error += f"- {file}\n"

    sink.send_error_message(str(error))

    sys.stdout.write("\r\n=== Error Analysis ===\r\n")
    print(json.dumps(analysis, indent=2))
    if analysis['error_found']:
        sys.stdout.write(f"Error Type: {analysis['error_type']}\r\n")
        sys.stdout.write(f"Error Message: {analysis['error_message']}\r\n")
        sys.stdout.write(f"Affected Files: {', '.join(analysis['affected_files'])}\r\n")
        sys.stdout.write(f"Triggering Command: {analysis['triggering_command']}\r\n")
    else:
        sys.stdout.write("No errors detected in the output.\r\n")

    sys.stdout.write("===================\r\n")
    sys.stdout.flush()

    parser.save_analysis(analysis)


def main():
    sink = HTTPErrorMessageSink()
    if DEBUG:
        open('debug.log', 'w').close()

    max_lines = 2000
    cmd_logger = CommandLogger(max_lines)

    # Create a new PTY
    main_fd, secondary_fd = pty.openpty()

    # Save original terminal settings if we're in a terminal
    if os.isatty(sys.stdin.fileno()):
        old_settings = termios.tcgetattr(sys.stdin.fileno())
    else:
        old_settings = None

    pid = os.fork()

    if pid == 0:
        try:
            os.setpgrp()

            os.close(main_fd)

            os.dup2(secondary_fd, sys.stdin.fileno())
            os.dup2(secondary_fd, sys.stdout.fileno())
            os.dup2(secondary_fd, sys.stderr.fileno())

            if secondary_fd > 2:
                os.close(secondary_fd)

            term_settings = termios.tcgetattr(sys.stdin.fileno())
            term_settings[3] = term_settings[3] | termios.ECHO | termios.ICANON
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, term_settings)

            os.execvp('bash', ['bash'])
        except Exception as e:
            print(f"Child process error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            os.close(secondary_fd)

            if os.isatty(sys.stdin.fileno()):
                tty.setraw(sys.stdin.fileno())

            parser = LLMParser()

            while True:
                rlist, _, _ = select.select([sys.stdin, main_fd], [], [])

                for fd in rlist:
                    if fd == sys.stdin:
                        try:
                            data = os.read(sys.stdin.fileno(), 1)
                            if not data:
                                return
                            if data in (b'\x10',):
                                if old_settings:
                                    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)

                                sys.stdout.write('\r⌛ ')
                                sys.stdout.flush()
                                analyze_error(sink, parser, cmd_logger)
                                sys.stdout.write('\r \r')
                                sys.stdout.flush()

                                if os.isatty(sys.stdin.fileno()):
                                    tty.setraw(sys.stdin.fileno())
                                continue

                            if DEBUG:
                                write_to_file('stdin.txt', data)
                            cmd_logger.append_to_command(data)

                            os.write(main_fd, data)
                        except OSError:
                            return

                    elif fd == main_fd:
                        try:
                            data = os.read(main_fd, 1024)
                            if not data:
                                return
                            os.write(sys.stdout.fileno(), data)

                            if DEBUG:
                                write_to_file('stdout.txt', data)

                            cmd_logger.append_to_output(data, 'stdout')

                        except OSError:
                            return

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Parent process error: {e}", file=sys.stderr)
        finally:
            if old_settings and os.isatty(sys.stdin.fileno()):
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)

            os.close(main_fd)

            _, status = os.waitpid(pid, 0)

            cmd_logger.save_to_file()

if __name__ == '__main__':
    main()