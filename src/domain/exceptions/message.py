from domain.exceptions.base import BaseAppException


class EmptyMessageException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be empty")


class TooLongMessageException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be longer than 1000 characters")
