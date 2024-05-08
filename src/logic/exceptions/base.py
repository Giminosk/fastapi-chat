from domain.exceptions.base import BaseAppException


class LogicException(BaseAppException):
    def __init__(self, message: str = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("Error occured while processing request")
