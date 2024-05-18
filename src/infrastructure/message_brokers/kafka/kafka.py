from dataclasses import dataclass
from typing import AsyncIterator

import orjson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def stop(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()

    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        self.consumer.subscribe(topics=[topic])

        async for msg in self.consumer:
            yield orjson.loads(msg.value)

    async def stop_consuming(self) -> None:
        await self.consumer.unsubscribe()

    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self.producer.send(topic=topic, key=key, value=value)
