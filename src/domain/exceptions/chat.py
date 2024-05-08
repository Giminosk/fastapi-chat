from domain.exceptions.base import BaseAppException


class EmptyTitleException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be empty")


class TooLongTitleException(BaseAppException):
    def __init__(self):
        super().__init__("Message cannot be longer than 100 characters")


class TitleStrartsWithNoCapital(BaseAppException):
    def __init__(self):
        super().__init__("Title should start with capital letter")
