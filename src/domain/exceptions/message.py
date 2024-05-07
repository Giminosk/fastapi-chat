from dataclasses import dataclass

from domain.exceptions.base import BaseAppException


@dataclass(eq=False)
class EmptyMessageException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be empty")


@dataclass(eq=False)
class TooLongMessageException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be longer than 1000 characters")
