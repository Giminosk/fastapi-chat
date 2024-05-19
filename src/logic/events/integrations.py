from dataclasses import dataclass

import orjson

from domain.events.base import BaseEvent
from logic.events.base import BaseEventHandler


@dataclass
class IntergrationEvent(BaseEvent):
    pass


@dataclass
class NewMessageReceivedFromBrokerEvent(BaseEvent):
    message_oid: str
    chat_oid: str
    message_text: str


@dataclass
class NewMessageReceivedFromBrokerEventHandler(
    BaseEventHandler[NewMessageReceivedFromBrokerEvent, None]
):
    async def handle(self, event: NewMessageReceivedFromBrokerEvent) -> None:
        return await self.connection_manager.send_all(
            key=event.chat_oid,
            message=orjson.dumps(event),
        )
