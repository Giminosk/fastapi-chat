import punq
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from api.v1.chats.filters import GetChatsFilters, GetMessagesFilters
from api.v1.chats.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetChatSchema,
    GetChatsResponseSchema,
    GetMessageSchema,
    GetMessagesResponseSchema,
)
from domain.exceptions.base import BaseAppException
from logic.commands.chat import CreateChatCommand, GetAllChatsCommand, GetChatCommand
from logic.commands.message import CreateMessageCommand, GetMessagesByChatOidCommand
from logic.init_container import init_container
from logic.mediator.mediator import Mediator

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: punq.Container = Depends(init_container),
) -> CreateChatResponseSchema:
    mediator = container.resolve(Mediator)
    command = CreateChatCommand(
        title=schema.title,
    )

    try:
        chat, *_ = await mediator.execute([command])
        return CreateChatResponseSchema(
            chat_oid=chat.oid,
            title=chat.title.as_generic_type(),
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)


@router.post(
    "/{chat_oid}/messages/",
    response_model=CreateMessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: punq.Container = Depends(init_container),
):
    mediator = container.resolve(Mediator)
    command = CreateMessageCommand(chat_oid=chat_oid, text=schema.text)

    try:
        message, *_ = await mediator.execute([command])
        return CreateMessageResponseSchema(
            chat_oid=chat_oid,
            message_oid=message.oid,
            text=message.text.as_generic_type(),
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)


@router.get(
    "/{chat_oid}/",
    response_model=GetChatSchema,
    status_code=status.HTTP_200_OK,
)
async def get_chat_handler(
    chat_oid: str,
    container: punq.Container = Depends(init_container),
):
    mediator = container.resolve(Mediator)
    command = GetChatCommand(chat_oid=chat_oid)

    try:
        chat, *_ = await mediator.execute([command])
        return GetChatSchema(
            chat_oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)


@router.get(
    "/{chat_oid}/messages/",
    response_model=GetMessagesResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_messages_by_chat_oid_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: punq.Container = Depends(init_container),
):
    mediator = container.resolve(Mediator)
    command = GetMessagesByChatOidCommand(
        chat_oid=chat_oid, filters=filters.as_infra_filter()
    )

    try:
        (messages, count), *_ = await mediator.execute([command])
        return GetMessagesResponseSchema(
            count=count,
            offset=filters.offset,
            limit=filters.limit,
            results=[
                GetMessageSchema(
                    message_oid=message.oid,
                    text=message.text.as_generic_type(),
                    created_at=message.created_at,
                    chat_oid=message.chat_oid,
                )
                for message in messages
            ],
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)


@router.get(
    "/",
    response_model=GetChatsResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_all_chats_handler(
    filters: GetChatsFilters = Depends(),
    container: punq.Container = Depends(init_container),
):
    mediator = container.resolve(Mediator)
    command = GetAllChatsCommand(filters=filters.as_infra_filter())

    try:
        (chats, count), *_ = await mediator.execute([command])
        return GetChatsResponseSchema(
            count=count,
            offset=filters.offset,
            limit=filters.limit,
            results=[
                GetChatSchema(
                    title=chat.title.as_generic_type(),
                    created_at=chat.created_at,
                    chat_oid=chat.oid,
                )
                for chat in chats
            ],
        )
    except BaseAppException as exception:
        raise HTTPException(status_code=400, detail=exception.message)
