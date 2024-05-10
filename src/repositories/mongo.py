from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient

from domain.entities.chat import Chat
from repositories.base import BaseChatRepository
from repositories.converters import converter_chat2json


@dataclass
class MongoChatRepository(BaseChatRepository):
    client: AsyncIOMotorClient
    database: str
    collection_name: str

    def _get_collection(self):
        return self.client[self.database][self.collection_name]

    async def save_chat(self, chat: Chat) -> None:
        collection = self._get_collection()
        await collection.insert_one(converter_chat2json(chat))

    async def get_chat_by_title(self, title: str) -> Chat | None:
        collection = self._get_collection()
        query_filter = {"title": title}
        return await collection.find_one(query_filter)

    async def delete_chat_by_title(self, title: str) -> None:
        collection = self._get_collection()
        query_filter = {"title": title}
        await collection.delete_one(query_filter)
