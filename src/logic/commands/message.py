from dataclasses import dataclass
from typing import Iterable

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.message import Text
from infrastructure.repositories.base import BaseChatRepository, BaseMessageRepository
from infrastructure.repositories.filters.message import GetMessagesFilters
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.chat import ChatNotFoundException


@dataclass
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    message_repository: BaseMessageRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat: Chat = await self.chat_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            raise ChatNotFoundException(oid=command.chat_oid)

        message = Message(
            text=Text(command.text),
            chat_oid=command.chat_oid,
        )

        await self.message_repository.save_message(
            chat_oid=command.chat_oid, message=message
        )

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
            chat_oid=command.chat_oid, filters=command.filters
        )
        return messages, count
