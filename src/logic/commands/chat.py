from dataclasses import dataclass
from typing import Iterable

from domain.entities.chat import Chat
from domain.values.chat import Title
from infrastructure.repositories.base import BaseChatRepository
from infrastructure.repositories.filters.chat import GetChatsFilters
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.chat import (
    ChatNotFoundException,
    ChatWithTitleAlreadyExistsException,
)


@dataclass
class CreateChatCommand(BaseCommand):
    title: str


@dataclass
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithTitleAlreadyExistsException(title=command.title)

        chat = Chat.create_chat(title=Title(command.title))

        await self.chat_repository.save_chat(chat)

        await self._mediator.publish(chat.pull_events())

        return chat


@dataclass
class GetChatCommand(BaseCommand):
    chat_oid: str


@dataclass
class GetChatCommandHandler(BaseCommandHandler[GetChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: GetChatCommand) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(oid=command.chat_oid)

        return chat


@dataclass
class GetAllChatsCommand(BaseCommand):
    filters: GetChatsFilters


@dataclass
class GetAllChatsCommandHandler(
    BaseCommandHandler[GetAllChatsCommand, tuple[Iterable[Chat], int]]
):
    chat_repository: BaseChatRepository

    async def handle(self, command: GetAllChatsCommand) -> tuple[list[Chat], int]:
        chats, count = await self.chat_repository.get_all_chats(filters=command.filters)
        return chats, count


@dataclass
class DeleteChatCommand(BaseCommand):
    chat_oid: str


@dataclass
class DeleteChatCommandHandler(BaseCommandHandler[DeleteChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: DeleteChatCommand) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(oid=command.chat_oid)

        await self.chat_repository.delete_chat_by_oid(oid=command.chat_oid)

        chat.delete_chat()
        await self._mediator.publish(chat.pull_events())

        return chat
