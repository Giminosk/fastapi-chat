import os
import uuid
from functools import lru_cache

import punq
from aiojobs import Scheduler
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from motor.motor_asyncio import AsyncIOMotorClient

from domain.events.chat import (
    ChatDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka.kafka import KafkaMessageBroker
from infrastructure.repositories.base import BaseChatRepository, BaseMessageRepository
from infrastructure.repositories.memory import MemoryChatRepository
from infrastructure.repositories.mongo.chat import MongoChatRepository
from infrastructure.repositories.mongo.message import MongoMessageRepository
from infrastructure.websockets.connection_manager import (
    BaseConnectionManager,
    ConnectionManager,
)
from logic.commands.chat import (
    CreateChatCommand,
    CreateChatCommandHandler,
    DeleteChatCommand,
    DeleteChatCommandHandler,
    GetAllChatsCommand,
    GetAllChatsCommandHandler,
    GetChatCommand,
    GetChatCommandHandler,
)
from logic.commands.message import (
    CreateMessageCommand,
    CreateMessageCommandHandler,
    GetMessagesByChatOidCommand,
    GetMessagesByChatOidCommandHandler,
)
from logic.events.chat import ChatDeletedEventHandler, NewChatCreatedEventHandler
from logic.events.integrations import (
    NewMessageReceivedFromBrokerEvent,
    NewMessageReceivedFromBrokerEventHandler,
)
from logic.events.message import NewMessageReceivedEventHandler
from logic.mediator.mediator import Mediator
from settings.config import Config


@lru_cache(1)
def init_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    # * Config
    container.register(
        Config,
        factory=lambda: Config(),
        scope=punq.Scope.singleton,
    )
    config: Config = container.resolve(Config)

    # * Mongo Client
    def _init_mongo_client():
        return AsyncIOMotorClient(config.mongo_uri, serverSelectionTimeoutMS=5000)

    container.register(
        AsyncIOMotorClient,
        factory=_init_mongo_client,
        scope=punq.Scope.singleton,
    )
    client = container.resolve(AsyncIOMotorClient)

    # * Repositories
    def _init_chat_repository() -> BaseChatRepository:
        if os.getenv("APP_ENV") == "test":
            return MemoryChatRepository()
        else:
            return MongoChatRepository(
                client=client,
                database=config.mongo_database,
                collection_name=config.mongo_chat_collection,
            )

    def _init_message_repository() -> BaseMessageRepository:
        if os.getenv("APP_ENV") == "test":
            return MemoryChatRepository()
        else:
            return MongoMessageRepository(
                client=client,
                database=config.mongo_database,
                collection_name=config.mongo_message_collection,
            )

    container.register(
        BaseChatRepository,
        factory=_init_chat_repository,
        scope=punq.Scope.singleton,
    )
    container.register(
        BaseMessageRepository,
        factory=_init_message_repository,
        scope=punq.Scope.singleton,
    )

    # * Message Broker (Kafka)
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
        BaseMessageBroker,
        factory=_init_message_broker,
        scope=punq.Scope.singleton,
    )

    # * Connection Manager
    container.register(
        BaseConnectionManager,
        factory=lambda: ConnectionManager(),
        scope=punq.Scope.singleton,
    )

    # * Command Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)
    container.register(GetChatCommandHandler)
    container.register(GetMessagesByChatOidCommandHandler)
    container.register(GetAllChatsCommandHandler)
    container.register(DeleteChatCommandHandler)

    # * Event Handlers
    container.register(NewChatCreatedEventHandler)
    container.register(NewMessageReceivedEventHandler)
    container.register(NewMessageReceivedFromBrokerEventHandler)
    container.register(ChatDeletedEventHandler)

    # * Mediator
    def _init_mediator() -> Mediator:
        mediator = Mediator()

        # * mediator command handlers
        create_chat_command_handler = CreateChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )
        create_message_command_handler = CreateMessageCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
            message_repository=container.resolve(BaseMessageRepository),
        )
        get_chat_command_handler = GetChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )
        get_messages_by_chat_oid_command_handler = GetMessagesByChatOidCommandHandler(
            _mediator=mediator,
            message_repository=container.resolve(BaseMessageRepository),
        )
        get_all_chats_command_handler = GetAllChatsCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )
        delete_chat_command_handler = DeleteChatCommandHandler(
            _mediator=mediator,
            chat_repository=container.resolve(BaseChatRepository),
        )

        # * mediator event handlers
        new_chat_created_event_handler = NewChatCreatedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
            topic=config.new_chat_created_event_topic,
        )
        new_message_recieved_even_handler = NewMessageReceivedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
            topic=config.new_message_recived_event_topic,
        )
        new_message_received_from_broker_event_handler = (
            NewMessageReceivedFromBrokerEventHandler(
                message_broker=container.resolve(BaseMessageBroker),
                connection_manager=container.resolve(BaseConnectionManager),
                topic=config.new_message_recived_event_topic,
            )
        )
        chat_deleted_event_handler = ChatDeletedEventHandler(
            message_broker=container.resolve(BaseMessageBroker),
            connection_manager=container.resolve(BaseConnectionManager),
            topic=config.chat_deleted_event_topic,
        )

        # * register up handlers in mediator
        mediator.register_command_handlers(
            command_type=CreateChatCommand,
            handlers=[create_chat_command_handler],
        )
        mediator.register_command_handlers(
            command_type=CreateMessageCommand,
            handlers=[create_message_command_handler],
        )
        mediator.register_command_handlers(
            command_type=GetChatCommand,
            handlers=[get_chat_command_handler],
        )
        mediator.register_command_handlers(
            command_type=GetMessagesByChatOidCommand,
            handlers=[get_messages_by_chat_oid_command_handler],
        )
        mediator.register_event_handlers(
            event_type=NewChatCreatedEvent,
            handlers=[new_chat_created_event_handler],
        )
        mediator.register_event_handlers(
            event_type=NewMessageReceivedEvent,
            handlers=[new_message_recieved_even_handler],
        )
        mediator.register_event_handlers(
            event_type=NewMessageReceivedFromBrokerEvent,
            handlers=[new_message_received_from_broker_event_handler],
        )
        mediator.register_command_handlers(
            command_type=GetAllChatsCommand,
            handlers=[get_all_chats_command_handler],
        )
        mediator.register_command_handlers(
            command_type=DeleteChatCommand,
            handlers=[delete_chat_command_handler],
        )
        mediator.register_event_handlers(
            event_type=ChatDeletedEvent,
            handlers=[chat_deleted_event_handler],
        )

        return mediator

    container.register(
        Mediator,
        factory=_init_mediator,
    )

    # * Scheduler
    container.register(
        Scheduler,
        factory=lambda: Scheduler(),
        scope=punq.Scope.singleton,
    )

    return container
