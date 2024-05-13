from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    title: str


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    chat_oid: str
    message_oid: str
    message_text: str
