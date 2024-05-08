from dataclasses import dataclass

from domain.entities.chat import Chat
from logic.commands.base import BaseCommand, BaseCommandHandler
from repositories.base import BaseChatRepository
from logic.exceptions.chat import ChatWithTitleAlreadyExistsException


@dataclass
class CreateChatCommand(BaseCommand):
    title: str


@dataclass
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if not bool(await self.chat_repository.get_chat_by_title(command.title)):
            raise ChatWithTitleAlreadyExistsException

        chat = Chat.create_chat(command.title)

        await self.chat_repository.save_chat(chat)

        return chat
