class WrongParamException(Exception):
    """
    Exception used when user parameter or body is wrong.
    """
    def __init__(self, message):
        super().__init__(message)
