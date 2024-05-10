from dataclasses import dataclass

import repositories.mongo.converters as converter
from domain.entities.message import Message
from repositories.base import BaseMessageRepository
from repositories.mongo.base import BaseMongoRepository


@dataclass
class MongoMessageRepository(BaseMongoRepository, BaseMessageRepository):
    async def save_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={
                "$push": {
                    "messages": converter.converte_message2json(message),
                },
            },
        )

    async def get_messages_by_chat_oid(self, chat_oid: str) -> list[Message]:
        query_filter = {"oid": chat_oid}
        messages = await self._collection.find_one(query_filter)["messages"]
        return [converter.converte_json2message(message) for message in messages]
