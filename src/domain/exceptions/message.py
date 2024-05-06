from dataclasses import dataclass

from domain.exceptions.base import BaseAppException


@dataclass
class EmptyMessageException(BaseAppException):
    @property
    def message(self):
        return "Message cannot be empty"


@dataclass
class TooLongMessageException(BaseAppException):
    @property
    def message(self):
        return "Message cannot be longer than 1000 characters"
