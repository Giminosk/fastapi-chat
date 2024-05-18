import orjson
import punq
from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

from infrastructure.managers.connection_manager import BaseConnectionManager
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
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)
    await websocket.send_text("You are now connected!")

    message_broker = container.resolve(BaseMessageBroker)
    config = container.resolve(Config)

    try:
        while True:
            async for msg in message_broker.start_consuming(
                config.new_message_recived_event_topic
            ):
                await connection_manager.send_all(
                    key=msg.chat_oid, message=orjson.dumps(msg)
                )

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
