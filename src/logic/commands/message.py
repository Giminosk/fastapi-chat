from dataclasses import dataclass
from typing import Iterable

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.message import Text
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.chat import ChatNotFoundException
from repositories.base import BaseChatRepository, BaseMessageRepository
from repositories.filters.message import GetMessagesFilters


@dataclass
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    message_repository: BaseMessageRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat: Chat = await self.chat_repository.get_chat_by_oid(command.chat_oid)
        if not chat:
            raise ChatNotFoundException(command.chat_oid)

        message = Message(Text(command.text), command.chat_oid)

        await self.message_repository.save_message(command.chat_oid, message)

        chat.add_message(message)
        await self._mediator.publish(chat.pull_events())

        return message


@dataclass
class GetMessagesByChatOidCommand(BaseCommand):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass
class GetMessagesByChatOidCommandHandler(
    BaseCommandHandler[GetMessagesByChatOidCommand, tuple[Iterable[Message], int]]
):
    message_repository: BaseMessageRepository

    async def handle(
        self, command: GetMessagesByChatOidCommand
    ) -> tuple[list[Message], int]:
        messages, count = await self.message_repository.get_messages_by_chat_oid(
            command.chat_oid, command.filters
        )
        return messages, count
