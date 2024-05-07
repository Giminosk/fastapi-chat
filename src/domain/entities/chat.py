from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.values.chat import Title
from domain.entities.message import Message


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: list[Message] = field(
        default_factory=list,
        kw_only=True,
    )

    def add_message(self, message: Message) -> None:
        self.messages.append(message)