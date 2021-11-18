class APIexception(Exception):
    def __init__(self, message, status_code=406):
        super().__init__(message)
        self.status_code = status_code