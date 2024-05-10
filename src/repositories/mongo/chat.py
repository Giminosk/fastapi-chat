from dataclasses import dataclass

from domain.entities.chat import Chat
from repositories.mongo.converters import converte_chat2json
from repositories.mongo.base import BaseChatRepository, BaseMongoRepository


@dataclass
class MongoChatRepository(BaseMongoRepository, BaseChatRepository):

    async def save_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(converte_chat2json(chat))

    async def get_chat_by_title(self, title: str) -> Chat | None:
        query_filter = {"title": title}
        return await self._collection.find_one(query_filter)

    async def delete_chat_by_title(self, title: str) -> None:
        query_filter = {"title": title}
        await self._collection.delete_one(query_filter)
