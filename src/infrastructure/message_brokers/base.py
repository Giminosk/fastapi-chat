from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseProducer(ABC):
    @abstractmethod
    async def send(self, **kwargs) -> None:
        pass


@dataclass
class BaseConsumer(ABC):
    @abstractmethod
    async def subscribe(self, **kwargs) -> Any:
        pass


@dataclass
class BaseMessageBroker(ABC):
    producer: BaseProducer
    consumer: BaseConsumer

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    async def start_consuming(self, topic: str) -> Any:
        pass

    @abstractmethod
    async def stop_consuming(self, topic: str) -> None:
        pass

    @abstractmethod
    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        pass
