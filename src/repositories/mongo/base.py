from abc import ABC, abstractmethod
from dataclasses import dataclass
from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.chat import Chat
from domain.entities.message import Message


@dataclass
class BaseMongoRepository(ABC):
    client: AsyncIOMotorClient
    database: str
    collection_name: str

    @property
    def _collection(self):
        return self.client[self.database][self.collection_name]


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


@dataclass
class BaseMessageRepository(ABC):
    @abstractmethod
    async def save_message(self, chat_oid: str, message: Message) -> None:
        pass

    @abstractmethod
    async def get_messages_by_chat_oid(self, chat_oid: str) -> list[Message]:
        pass
