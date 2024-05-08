from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent

ET = TypeVar("ET", bound=BaseEvent)  # Event type
ER = TypeVar("ER", bound=Any)  # Event resutl


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    @abstractmethod
    async def handle(self, event: ET) -> ER:
        pass
