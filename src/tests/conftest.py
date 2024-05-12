import os

import punq
from pytest import fixture

from logic.init_container import _init_container
from logic.mediator.mediator import Mediator
from repositories.base import BaseChatRepository
from repositories.memory import MemoryChatRepository

os.environ["APP_ENV"] = "test"


@fixture(scope="function")
def container() -> punq.Container:
    container = _init_container()
    container.register(
        BaseChatRepository, MemoryChatRepository, scope=punq.Scope.singleton
    )
    return container


@fixture(scope="function")
def chat_repository(container: punq.Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@fixture(scope="function")
def mediator(container: punq.Container) -> Mediator:
    return container.resolve(Mediator)
