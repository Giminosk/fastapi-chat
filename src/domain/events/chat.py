from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class ChatCreated(BaseEvent):
    chat_oid: str
    title: str
    

@dataclass
class NewMessageReceived(BaseEvent):
    chat_oid: str
    message_oid: str
    message_text: str