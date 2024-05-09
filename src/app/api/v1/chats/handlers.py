from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.api.v1.chats.schemas import (CreateChatRequestHandler,
                                      CreateChatResponseHandler)
from domain.exceptions.base import BaseAppException
from logic.commands.chat import CreateChatCommand
from logic.mediator import Mediator
from settings.init_container import container

router = APIRouter(tags=["Chat"])


@router.post("/create", response_model=CreateChatResponseHandler)
async def create_chat(schema: CreateChatRequestHandler) -> CreateChatResponseHandler:
    mediator = container.resolve(Mediator)
    command = CreateChatCommand(schema.title)
    try:
        chat, *_ = await mediator.execute([command])
        return CreateChatResponseHandler(chat_oid=chat.oid, title=chat.title.value)
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)
