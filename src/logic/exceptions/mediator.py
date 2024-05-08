from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    def __init__(self, event_type: type):
        super().__init__(f"Could not find event handlers for {event_type}")


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    def __init__(self, command_type: type):
        super().__init__(f"Could not find command handlers for {command_type}")
