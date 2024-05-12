from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from domain.events.base import BaseEvent
from logic.events.base import ER, ET, EventHandler


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[ET : list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    @abstractmethod
    def register_event_handlers(
        self, event_type: ET, handlers: Iterable[EventHandler]
    ) -> None:
        pass

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> list[ER]:
        pass
