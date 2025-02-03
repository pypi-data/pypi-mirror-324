
class BaseErrorMessageSink:
    def __init__(self):
        self.error_messages = []

    def send_error_message(self, error_message):
        pass