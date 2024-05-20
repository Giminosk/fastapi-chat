from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.message import Message
from domain.events.chat import (
    ChatDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from domain.values.chat import Title


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: list[Message] = field(
        default_factory=list,
        kw_only=True,
    )
    is_deleted: bool = field(
        default=False,
        kw_only=True,
    )

    def add_message(self, message: Message) -> None:
        message.chat_oid = self.oid
        self.messages.append(message)
        self.add_event(
            NewMessageReceivedEvent(
                chat_oid=self.oid,
                message_oid=message.oid,
                message_text=message.text.as_generic_type(),
            ),
        )

    @classmethod
    def create_chat(cls, title: Title, messages: list[Message] = None) -> "Chat":
        chat = cls(title=title)
        chat.add_event(
            NewChatCreatedEvent(
                chat_oid=chat.oid,
                title=title.as_generic_type(),
            ),
        )
        if messages is not None:
            for message in messages:
                chat.add_message(message)
        return chat

    def delete_chat(self) -> None:
        self.is_deleted = True
        self.add_event(
            ChatDeletedEvent(
                chat_oid=self.oid,
                title=self.title.as_generic_type(),
            ),
        )
