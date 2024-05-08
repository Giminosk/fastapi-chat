from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from domain.events.base import BaseEvent
from logic.commands.base import CR, CT, BaseCommand, CommandHandler
from logic.events.base import ER, ET, EventHandler
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    EventHandlersNotRegisteredException,
)


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET : list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )
    commands_map: dict[CT : list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def register_event_handlers(
        self, event_type: ET, handlers: Iterable[EventHandler]
    ) -> None:
        self.events_map[event_type].extend(handlers)

    def register_command_handlers(
        self, command_type: CT, handlers: Iterable[CommandHandler]
    ) -> None:
        self.commands_map[command_type].extend(handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> list[ER]:
        results = []
        for event in events:
            event_handlers = self.events_map[type(event)]
            if not event_handlers:
                raise EventHandlersNotRegisteredException(type(event))
            for event_handler in event_handlers:
                result = await event_handler.handle(event)
                results.append(result)
        return results

    async def execute(self, commands: Iterable[BaseCommand]) -> list[CR]:
        results = []
        for command in commands:
            command_handlers = self.commands_map[type(command)]
            if not command_handlers:
                raise CommandHandlersNotRegisteredException(type(command))
            for command_handler in command_handlers:
                result = await command_handler.handle(command)
                results.append(result)
        return results
