from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithTitleAlreadyExistsException(LogicException):
    title: str

    def __init__(self, title: str):
        super().__init__(f"Chat with title {title} already exists")
