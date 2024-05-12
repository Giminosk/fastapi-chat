import os
from functools import lru_cache

import punq
from motor.motor_asyncio import AsyncIOMotorClient

from logic.commands.chat import (
    CreateChatCommand,
    CreateChatCommandHandler,
    GetChatCommand,
    GetChatCommandHandler,
)
from logic.commands.message import (
    CreateMessageCommand,
    CreateMessageCommandHandler,
    GetMessagesByChatOidCommand,
    GetMessagesByChatOidCommandHandler,
)
from logic.mediator.mediator import Mediator
from repositories.base import BaseChatRepository, BaseMessageRepository
from repositories.memory import MemoryChatRepository
from repositories.mongo.chat import MongoChatRepository
from repositories.mongo.message import MongoMessageRepository
from settings.dbconfig import DBConfig


@lru_cache(1)
def init_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    # * Config
    container.register(DBConfig, factory=lambda: DBConfig(), scope=punq.Scope.singleton)
    config = container.resolve(DBConfig)

    # * Client
    def _init_mongo_client():
        return AsyncIOMotorClient(config.mongo_uri, serverSelectionTimeoutMS=5000)

    container.register(
        AsyncIOMotorClient, factory=_init_mongo_client, scope=punq.Scope.singleton
    )
    client = container.resolve(AsyncIOMotorClient)

    # * Repositories
    def _init_chat_repository() -> BaseChatRepository:
        if os.getenv("APP_ENV") == "test":
            return MemoryChatRepository()
        else:
            return MongoChatRepository(
                client,
                config.mongo_database,
                config.mongo_chat_collection,
            )

    def _init_message_repository() -> BaseMessageRepository:
        if os.getenv("APP_ENV") == "test":
            return MemoryChatRepository()
        else:
            return MongoMessageRepository(
                client,
                config.mongo_database,
                config.mongo_message_collection,
            )

    container.register(
        BaseChatRepository, factory=_init_chat_repository, scope=punq.Scope.singleton
    )
    container.register(
        BaseMessageRepository,
        factory=_init_message_repository,
        scope=punq.Scope.singleton,
    )

    # * Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(GetChatCommandHandler)
    container.register(GetMessagesByChatOidCommandHandler)

    # * Mediator
    def _init_mediator() -> Mediator:
        mediator = Mediator()

        create_chat_command_handler = CreateChatCommandHandler(
            _mediator=mediator, chat_repository=container.resolve(BaseChatRepository)
        )
        create_message_command_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
            message_repository=container.resolve(BaseMessageRepository),
        )
        get_chat_command_handler = GetChatCommandHandler(
            _mediator=mediator, chat_repository=container.resolve(BaseChatRepository)
        )
        get_messages_by_chat_oid_command_handler = GetMessagesByChatOidCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessageRepository),
        )

        mediator.register_command_handlers(
            CreateChatCommand, [create_chat_command_handler]
        )
        mediator.register_command_handlers(
            CreateMessageCommand, [create_message_command_handler]
        )
        mediator.register_command_handlers(GetChatCommand, [get_chat_command_handler])
        mediator.register_command_handlers(
            GetMessagesByChatOidCommand,
            [get_messages_by_chat_oid_command_handler],
        )
        return mediator

    container.register(Mediator, factory=_init_mediator)

    return container
