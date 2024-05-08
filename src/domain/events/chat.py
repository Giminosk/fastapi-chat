from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class ChatCreatedEvent(BaseEvent):
    chat_oid: str
    title: str


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    chat_oid: str
    message_oid: str
    message_text: str
