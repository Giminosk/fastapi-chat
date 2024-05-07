from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.chat import ChatCreated, NewMessageReceived
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
        self.add_event(
            NewMessageReceived(
                chat_oid=self.oid,
                message_oid=message.oid,
                message_text=message.text.as_generic_type(),
            ),
        )

    @classmethod
    def create_chat(cls, title: Title, messages: list[Message] = None) -> "Chat":
        chat = cls(title=title)
        chat.add_event(
            ChatCreated(
                chat_oid=chat.oid,
                title=title.as_generic_type(),
            ),
        )
        if messages is not None:
            for message in messages:
                chat.add_message(message)
        return chat
