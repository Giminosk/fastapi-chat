from abc import ABC
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.events.base import BaseEvent


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    events: list[BaseEvent] = field(
        default_factory=list,
        kw_only=True,
    )

    def add_event(self, event: BaseEvent) -> None:
        self.events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        events = copy(self.events)
        self.events = []
        return events

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseEntity):
            return self.oid == other.oid
        return False
