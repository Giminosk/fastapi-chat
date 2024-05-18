from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1.chats.handlers import router as chat_router
from api.v1.websockets.chats import router as chat_ws_router
from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init_container import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    broker = container.resolve(BaseMessageBroker)
    await broker.start()

    yield

    await broker.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Chat",
        docs_url="/api/v1/docs/",
        debug=True,
        lifespan=lifespan,
    )

    app.include_router(chat_router, prefix="/chat")
    app.include_router(chat_ws_router, prefix="/chat")

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
