import orjson
import punq
from fastapi import Depends, WebSocket
from fastapi.routing import APIRouter

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init_container import init_container
from settings.config import Config

router = APIRouter(tags=["Chat"])


@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    chat_oid: str,
    websocket: WebSocket,
    container: punq.Container = Depends(init_container),
):
    await websocket.accept()
    await websocket.send_text("You are now connected!")

    message_broker = container.resolve(BaseMessageBroker)
    config = container.resolve(Config)

    while True:
        async for msg in message_broker.start_consuming(
            config.new_message_recived_event_topic
        ):
            await websocket.send_bytes(orjson.dumps(msg))
