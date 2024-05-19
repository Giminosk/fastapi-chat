from contextlib import asynccontextmanager

from aiojobs import Scheduler
from fastapi import FastAPI

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.events.integrations import NewMessageReceivedFromBrokerEvent
from logic.init_container import init_container
from logic.mediator.mediator import Mediator
from settings.config import Config


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()

    broker = container.resolve(BaseMessageBroker)
    await broker.start()

    scheduler: Scheduler = container.resolve(Scheduler)
    job = await scheduler.spawn(consume_messages_in_background())

    yield

    await broker.stop()
    await job.close()


async def consume_messages_in_background():
    container = init_container()
    message_broker = container.resolve(BaseMessageBroker)
    config = container.resolve(Config)
    mediator: Mediator = container.resolve(Mediator)

    async for msg in message_broker.start_consuming(
        config.new_message_recived_event_topic
    ):
        await mediator.publish(
            [
                NewMessageReceivedFromBrokerEvent(
                    chat_oid=msg["chat_oid"],
                    message_oid=msg["message_oid"],
                    message_text=msg["message_text"],
                )
            ]
        )
