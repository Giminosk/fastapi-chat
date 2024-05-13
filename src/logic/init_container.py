import os
import uuid
from functools import lru_cache

import punq
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient

from domain.events.chat import NewChatCreatedEvent
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
from logic.events.chat import NewChatCreatedEventHandler
from logic.mediator.mediator import Mediator
from message_brokers.base import BaseMessageBroker
from message_brokers.kafka.kafka import KafkaMessageBroker
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
    config: DBConfig = container.resolve(DBConfig)

    # * Mongo Client
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

    # * Message Broker
    def _init_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(
                bootstrap_servers=config.kafka_uri,
            ),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_uri,
                group_id=f"chats-{uuid.uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )

    container.register(
        BaseMessageBroker, factory=_init_message_broker, scope=punq.Scope.singleton
    )

    # * Command Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(GetChatCommandHandler)
    container.register(GetMessagesByChatOidCommandHandler)

    # * Event Handlers
    container.register(NewChatCreatedEventHandler)

    # * Mediator
    def _init_mediator() -> Mediator:
        mediator = Mediator()

        # * mediator command handlers
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

        # * mediator event handlers
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            topic=config.new_chat_created_event_topic,
        )

        # * register up handlers in mediator
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
        mediator.register_event_handlers(
            NewChatCreatedEvent, [new_chat_created_event_handler]
        )
        return mediator

    container.register(Mediator, factory=_init_mediator)

    return container
