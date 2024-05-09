import uvicorn
from fastapi import FastAPI

from app.api.v1.chats.handlers import router as chat_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Chat",
        docs_url="/api/v1/docs",
        debug=True,
    )

    app.include_router(chat_router, prefix="/chat")

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
