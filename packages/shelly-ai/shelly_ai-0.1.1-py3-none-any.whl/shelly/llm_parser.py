#!/usr/bin/env python3
import json
from typing import Dict
from litellm import acompletion


class LLMParser:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    async def analyze_error(self, cmd_history: Dict) -> Dict:
        """
        Analyze the command output for errors using LLM.
        Only analyzes the output from the most recent command.
        """
        command = cmd_history.get('last_command', '')
        current_output = cmd_history.get('current_output', '')

        prompt = f"""You are a Unix shell error analyzer. Analyze this command output for errors.
Important: Normal command output that displays information is NOT an error, even if it shows system details, process information, or status reports.

Only report an error if you see explicit error indicators like:
- "command not found"
- "permission denied"
- "no such file or directory" 
- Stack traces
- Compilation errors
- Runtime exceptions
- Syntax errors


Command executed: {command}

Output:
{current_output}

Return a JSON object containing a COMPLETE analysis of ALL errors found in the output. You must:

1. Identify every distinct error message, not just the final or fatal error
2. For compiler errors, include the full context:
   - File path
   - Line number
   - Column number
   - The specific error message
   - The code snippet if shown
3. For build system errors (like make errors), capture:
   - The full error message
   - The affected targets
   - The error type
   
Format your response as JSON with these fields:
- error_found: boolean indicating if any explicit errors were found
- error_messages: list of ALL distinct error messages found in the following format:  
   -- message: the error message
   -- file_path: the file path where the error occurred
   -- line_number: the line number where the error occurred
- affected_files: array of files mentioned in error messages
- triggering_command: the command that caused the error
- error_type: type of error (build/runtime/syntax/permission/etc), or null if no error
- root_cause: the root cause of the error, or null if no error
Remember: Only report errors when there are clear error messages or failure indicators. 

Common patterns that indicate VALID output (not errors):
- Table-like output showing system status
- Lists of processes, users, or resources
- Statistics and metrics
- Version information
- Help text or command usage info
- Empty output or simple status reports

DO NOT include duplicated error messages or generic error messages that don't provide useful information. 
For example, this should be added only as a single error message:
```
 1. Compiling of foo.cpp failed.
 2. Compiling of foo.cpp lead to linking error
 3. linking error lead to failed make command
```

Untitled

DO NOT include cascading build system messages that result from a single root cause. Only include the original error message that caused the build failure. For build/compilation errors:

1. Only include the actual compiler error message with its location and context
2. Ignore subsequent build system messages (like make/cmake errors) that are just reporting the propagation of the original failure
3. Don't include error exit codes or "Error N" messages from the build system

For example, if you see this output:
```
foo.cpp:10:5: error: undefined reference to 'bar'
make[2]: *** [foo.o] Error 1
make[1]: *** [all] Error 2
make: *** [all] Error 2
```
Only include the first error message "undefined reference to 'bar'" in the error_messages list, since the make errors are just reporting the cascade from that root cause.

For example:
It is not an error if the output is the user calls "cat error.log" and the output is "No such file or directory".
    It is an error if the output is the user calls "gcc -o hello hello.c" and the output is "syntax error: missing semicolon".
    It is not an error if the output is the user calls "ps aux" and the output shows a list of running processes.
    It is an error if the output is the user calls "chmod 777 /etc/passwd" and the output is "Permission denied".
    It is not an error if the output is the user calls "df -h" and the output shows disk usage statistics.
    It is an error if the output is the user calls "python script.py" and the output shows "IndentationError: unexpected indent".
    It is not an error if the output is the user calls "git status" and the output shows "nothing to commit, working tree clean".
    It is an error if the output is the user calls "npm install" and the output contains "Error: ENOENT: no such file or directory, open 'package.json'".
    It is not an error if the output is the user calls "top" and the output shows system resource usage.
    It is an error if the output is the user calls "docker run myimage" and the output is "Error response from daemon: pull access denied".
    It is not an error if the output is the user calls "netstat -an" and the output shows network connections.
    It is an error if the output is the user calls "java MyClass.java" and the output contains "Exception in thread 'main' java.lang.NullPointerException".
    It is not an error if the output is the user calls "who" and the output shows currently logged-in users.
    It is an error if the output is the user calls "mv file1 file2" and the output is "mv: cannot stat 'file1': No such file or directory".
    It is not an error if the output is the user calls "ls -la" and the output shows file permissions and timestamps.

If the output follows normal formatting and doesn't contain explicit error messages, it's not an error."""

        try:
            response = await acompletion(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                response_format={"type": "json_object"},
            )

            analysis = json.loads(response.choices[0].message.content)

            required_fields = ['error_found', 'error_message', 'affected_files',
                               'triggering_command', 'error_type']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = None if field != 'affected_files' else []

        except Exception as e:
            analysis = {
                "error_found": False,
                "error_message": f"Failed to analyze output: {str(e)}",
                "affected_files": [],
                "triggering_command": command,
                "error_type": None
            }

        return analysis

    def save_analysis(self, analysis: Dict, filename: str = 'error_analysis.json'):
        """Save the error analysis results to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, indent=2, fp=f)