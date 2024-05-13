from dataclasses import dataclass

import orjson

from domain.events.chat import NewChatCreatedEvent
from logic.events.base import BaseEventHandler


@dataclass
class NewChatCreatedEventHandler(BaseEventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        return await self.message_broker.send_message(
            topic=self.topic,
            key=event.eid.encode(),
            value=orjson.dumps(event),
        )
