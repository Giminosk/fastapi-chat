from dataclasses import dataclass

import repositories.mongo.converters as converter
from domain.entities.message import Message
from repositories.base import BaseMessageRepository
from repositories.filters.message import GetMessagesFilters
from repositories.mongo.base import BaseMongoRepository


@dataclass
class MongoMessageRepository(BaseMongoRepository, BaseMessageRepository):
    async def save_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.insert_one(converter.converte_message2json(message))

    async def get_messages_by_chat_oid(
        self, chat_oid: str, filters: GetMessagesFilters
    ) -> list[Message]:
        query_filter = {"chat_oid": chat_oid}

        count = await self._collection.count_documents(query_filter)

        cursor = (
            self._collection.find(query_filter)
            .skip(count - filters.limit - filters.offset)
            .limit(filters.limit)
        )
        messages = [
            converter.converte_json2message(message) async for message in cursor
        ]

        return messages, count
