from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass
class BaseCommand(ABC):
    pass


CT = TypeVar("CT", bound=BaseCommand)  # Command type
CR = TypeVar("CR", bound=Any)  # Command result


@dataclass
class CommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    async def handle(self, command: CT) -> CR:
        pass
