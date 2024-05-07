from dataclasses import dataclass

from domain.exceptions.base import BaseAppException


@dataclass(eq=False)
class EmptyTitleException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be empty")


@dataclass(eq=False)
class TooLongTitleException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be longer than 100 characters")


@dataclass(eq=False)
class TitleStrartsWithNoCapital(BaseAppException):
    def __init__(self):
        super().__init__("Title should start with capital letter")
