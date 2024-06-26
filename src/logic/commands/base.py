from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from logic.mediator.event import EventMediator


@dataclass
class BaseCommand(ABC):
    pass


CT = TypeVar("CT", bound=BaseCommand)  # Command type
CR = TypeVar("CR", bound=Any)  # Command result


@dataclass
class BaseCommandHandler(ABC, Generic[CT, CR]):
    _mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
