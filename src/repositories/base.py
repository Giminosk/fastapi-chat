from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.chat import Chat


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def save_chat(self, chat: Chat) -> None:
        pass

    @abstractmethod
    async def get_chat_by_title(self, title: str) -> Chat | None:
        pass

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self.get_chat_by_title(title))

    @abstractmethod
    async def delete_chat_by_title(self, title: str) -> None:
        pass
