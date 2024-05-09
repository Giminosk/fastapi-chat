from dataclasses import dataclass

from domain.entities.chat import Chat
from domain.values.chat import Title
from logic.commands.base import BaseCommand, BaseCommandHandler
from logic.exceptions.chat import ChatWithTitleAlreadyExistsException
from repositories.base import BaseChatRepository


@dataclass
class CreateChatCommand(BaseCommand):
    title: str


@dataclass
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithTitleAlreadyExistsException(command.title)

        chat = Chat.create_chat(Title(command.title))

        await self.chat_repository.save_chat(chat)

        return chat
