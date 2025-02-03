import os
import requests
import uuid
from datetime import datetime
from .base_error_messag_sink import BaseErrorMessageSink


class HTTPErrorMessageSink(BaseErrorMessageSink):
    def __init__(self):
        super().__init__()
        in_docker = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')
        self.server_url = 'http://host.docker.internal:5002' if in_docker else 'http://localhost:5002'
        self.api_endpoint = f"{self.server_url}/api/send_message"

        try:
            self._test_connection()
            print("Successfully connected to server!")
        except Exception as e:
            print(f"Failed to connect to server: {e}")

    def _test_connection(self):
        """Test the connection to the server with a simple request"""
        response = requests.get(self.server_url)
        response.raise_for_status()

    def send_error_message(self, error_message):
        try:
            message = {
                'id': str(uuid.uuid4()),
                'content': error_message,
                'msg_type': 'error',
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'completed',
                'requires_resolution': False,
                'resolution_id': None,
                'parent_id': None,
                'metadata': {}
            }

            print(f"Sending error message: {message}")

            response = requests.post(
                self.api_endpoint,
                json={'content': error_message},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )

            # Check if request was successful
            response.raise_for_status()

            # Store the error message locally
            self.error_messages.append(error_message)

            print(f"Server response: {response.text}")
            return response.json()

        except requests.RequestException as e:
            print(f"Failed to send error message: {e}")
            self.error_messages.append(error_message)
            return None

    def __del__(self):
        # No cleanup needed for HTTP implementation
        pass
