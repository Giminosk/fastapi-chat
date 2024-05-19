import punq
from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

from infrastructure.websockets.connection_manager import BaseConnectionManager
from logic.init_container import init_container

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

    try:
        while True:
            # listening to remain connection opened
            await websocket.receive_text()

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
