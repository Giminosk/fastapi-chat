import punq
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from app.api.v1.chats.schemas import (CreateChatRequestHandler,
                                      CreateChatResponseHandler,
                                      CreateMessageRequestHandler,
                                      CreateMessageResponseHandler)
from domain.exceptions.base import BaseAppException
from logic.commands.chat import CreateChatCommand
from logic.commands.message import CreateMessageCommand
from logic.mediator import Mediator
from settings.init_container import init_container

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    response_model=CreateChatResponseHandler,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_handler(
    schema: CreateChatRequestHandler,
    container: punq.Container = Depends(init_container),
) -> CreateChatResponseHandler:
    mediator = container.resolve(Mediator)
    command = CreateChatCommand(title=schema.title)
    try:
        chat, *_ = await mediator.execute([command])
        return CreateChatResponseHandler(
            chat_oid=chat.oid, title=chat.title.as_generic_type()
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)


@router.post(
    "/{chat_oid}/messages",
    response_model=CreateMessageResponseHandler,
    status_code=status.HTTP_201_CREATED,
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestHandler,
    container: punq.Container = Depends(init_container),
):
    mediator = container.resolve(Mediator)
    command = CreateMessageCommand(chat_oid=chat_oid, text=schema.text)
    try:
        message, *_ = await mediator.execute([command])
        return CreateMessageResponseHandler(
            chat_oid=chat_oid,
            message_oid=message.oid,
            text=message.text.as_generic_type(),
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)
