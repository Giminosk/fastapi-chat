from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class BaseMessageBroker(ABC):
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
