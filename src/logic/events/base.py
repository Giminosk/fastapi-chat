from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent
from message_brokers.base import BaseMessageBroker

ET = TypeVar("ET", bound=BaseEvent)  # Event type
ER = TypeVar("ER", bound=Any)  # Event resutl


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    topic: str | None = None

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        pass
