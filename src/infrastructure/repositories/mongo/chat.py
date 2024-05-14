from dataclasses import dataclass

import infrastructure.repositories.mongo.converters as converter
from domain.entities.chat import Chat
from infrastructure.repositories.base import BaseChatRepository
from infrastructure.repositories.mongo.base import BaseMongoRepository


@dataclass
class MongoChatRepository(BaseMongoRepository, BaseChatRepository):
    async def save_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(converter.converte_chat2json(chat))

    async def get_chat_by_title(self, title: str) -> Chat | None:
        query_filter = {"title": title}
        chat = await self._collection.find_one(query_filter)
        if chat is None:
            return None
        return converter.converte_json2chat(chat)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        query_filter = {"oid": oid}
        chat = await self._collection.find_one(query_filter)
        if chat is None:
            return None
        return converter.converte_json2chat(chat)

    async def delete_chat_by_title(self, title: str) -> None:
        query_filter = {"title": title}
        await self._collection.delete_one(query_filter)
