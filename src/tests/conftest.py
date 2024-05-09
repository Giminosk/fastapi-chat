import punq
from pytest import fixture

from logic.mediator import Mediator
from repositories.base import BaseChatRepository
from settings.init_container import init_container


@fixture(scope="function")
def container() -> punq.Container:
    container = init_container()
    return container


@fixture(scope="function")
def chat_repository(container: punq.Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)


@fixture(scope="function")
def mediator(container: punq.Container) -> Mediator:
    return container.resolve(Mediator)
