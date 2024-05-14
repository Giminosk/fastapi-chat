from dataclasses import dataclass

import infrastructure.repositories.mongo.converters as converter
from domain.entities.message import Message
from infrastructure.repositories.base import BaseMessageRepository
from infrastructure.repositories.filters.message import GetMessagesFilters
from infrastructure.repositories.mongo.base import BaseMongoRepository


@dataclass
class MongoMessageRepository(BaseMongoRepository, BaseMessageRepository):
    async def save_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.insert_one(converter.converte_message2json(message))

    async def get_messages_by_chat_oid(
        self, chat_oid: str, filters: GetMessagesFilters
    ) -> list[Message]:
        query_filter = {"chat_oid": chat_oid}

        count = await self._collection.count_documents(query_filter)
        skip = count - filters.limit - filters.offset
        cursor = (
            self._collection.find(query_filter)
            .skip(skip if skip > 0 else 0)
            .limit(filters.limit)
        )
        messages = [
            converter.converte_json2message(message) async for message in cursor
        ]

        return messages, count
