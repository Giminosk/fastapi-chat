from dataclasses import dataclass

from domain.entities.message import Message
from domain.values.message import Text
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.chat import ChatNotFoundException
from repositories.base import BaseChatRepository, BaseMessageRepository


@dataclass
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, Message]):
    message_repository: BaseMessageRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chat_repository.get_chat_by_oid(command.chat_oid)
        if not chat:
            raise ChatNotFoundException(command.chat_oid)

        message = Message(Text(command.text), command.chat_oid)

        await self.message_repository.save_message(command.chat_oid, message)

        return message
