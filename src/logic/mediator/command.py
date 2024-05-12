from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from logic.commands.base import CR, CT, BaseCommand, BaseCommandHandler


@dataclass(eq=False)
class CommandMediator(ABC):
    commands_map: dict[CT : list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    @abstractmethod
    def register_command_handlers(
        self, command_type: CT, handlers: Iterable[BaseCommandHandler]
    ) -> None:
        pass

    @abstractmethod
    async def execute(self, commands: Iterable[BaseCommand]) -> list[CR]:
        pass
