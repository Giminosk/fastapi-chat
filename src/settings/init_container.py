import os
from functools import lru_cache

import punq
from motor.motor_asyncio import AsyncIOMotorClient

from logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from repositories.base import BaseChatRepository
from repositories.memory import MemoryChatRepository
from repositories.mongo import MongoChatRepository
from settings.dbconfig import DBConfig


@lru_cache(1)
def init_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()
    container.register(DBConfig, factory=lambda: DBConfig(), scope=punq.Scope.singleton)
    container.register(CreateChatCommandHandler)

    def _init_repository() -> BaseChatRepository:
        if os.getenv("APP_ENV") == "test":
            return MemoryChatRepository()
        else:
            config = container.resolve(DBConfig)
            return MongoChatRepository(
                AsyncIOMotorClient(config.mongo_uri, serverSelectionTimeoutMS=5000),
                config.mongo_database,
                config.mongo_collection,
            )

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
