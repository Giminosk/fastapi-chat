from logic.exceptions.base import LogicException


class ChatWithTitleAlreadyExistsException(LogicException):
    def __init__(self, title: str):
        super().__init__(f"Chat with title <{title}> already exists")
