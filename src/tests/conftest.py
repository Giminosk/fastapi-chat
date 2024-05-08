from pytest import fixture

from logic.init_mediator import init_mediator
from logic.mediator import Mediator
from repositories.base import BaseChatRepository
from repositories.memory import MemoryChatRepository


@fixture(scope="function")
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@fixture(scope="function")
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator, chat_repository)
    return mediator
