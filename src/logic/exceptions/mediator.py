from logic.exceptions.base import LogicException


class EventHandlersNotRegisteredException(LogicException):
    event_type: type

    def __init__(self, event_type: type):
        super().__init__(f"Could not find event handlers for {event_type}")


class CommandHandlersNotRegisteredException(LogicException):
    def __init__(self, command_type: type):
        super().__init__(f"Could not find command handlers for {command_type}")
