import punq

from logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from repositories.base import BaseChatRepository
from repositories.memory import MemoryChatRepository


def init_container() -> punq.Container:
    container = punq.Container()
    container.register(CreateChatCommandHandler)

    def _init_repository() -> BaseChatRepository:
        return MemoryChatRepository()

    def _init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command_handlers(
            CreateChatCommand, [container.resolve(CreateChatCommandHandler)]
        )
        return mediator

    container.register(
        BaseChatRepository, factory=_init_repository, scope=punq.Scope.singleton
    )
    container.register(Mediator, factory=_init_mediator)

    return container
