from domain.values.chat import Title
from logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator
from repositories.base import BaseChatRepository
from repositories.memory import MemoryChatRepository


def init_mediator(mediator: Mediator, chat_repository: BaseChatRepository):
    mediator.register_command_handlers(
        CreateChatCommand, [CreateChatCommandHandler(chat_repository)]
    )
