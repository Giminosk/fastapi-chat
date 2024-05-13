from dataclasses import dataclass

import orjson

from domain.events.chat import NewMessageReceivedEvent
from logic.events.base import BaseEventHandler


@dataclass
class NewMessageReceivedEventHandler(BaseEventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        return await self.message_broker.send_message(
            topic=self.topic,
            key=event.eid.encode(),
            value=orjson.dumps(event),
        )
