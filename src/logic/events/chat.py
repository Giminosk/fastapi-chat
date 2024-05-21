from dataclasses import dataclass

import orjson

from domain.events.chat import ChatDeletedEvent, NewChatCreatedEvent
from logic.events.base import BaseEventHandler


@dataclass
class NewChatCreatedEventHandler(BaseEventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        return await self.message_broker.send_message(
            topic=self.topic,
            key=event.chat_oid.encode(),
            value=orjson.dumps(event),
        )


@dataclass
class ChatDeletedEventHandler(BaseEventHandler[ChatDeletedEvent, None]):
    async def handle(self, event: ChatDeletedEvent) -> None:
        await self.connection_manager.disconnect_all(key=event.chat_oid)
        return await self.message_broker.send_message(
            topic=self.topic,
            key=event.chat_oid.encode(),
            value=orjson.dumps(event),
        )
