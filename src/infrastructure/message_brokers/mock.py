import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import AsyncIterator

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class MockMessageBroker(BaseMessageBroker):
    messages: dict[str, list[dict]] = field(default_factory=lambda: defaultdict(list))

    def __post_init__(self):
        if self.messages is None:
            self.messages = {}

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        while True:
            if self.messages[topic]:
                yield self.messages[topic].pop(0)
            else:
                await asyncio.sleep(0.1)

    async def stop_consuming(self) -> None:
        pass

    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        self.messages[topic].append({"key": key, "value": value})
