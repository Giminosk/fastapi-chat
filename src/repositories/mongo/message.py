from dataclasses import dataclass

from domain.entities.message import Message
from repositories.mongo.converters import converte_message2json
from repositories.mongo.base import BaseMessageRepository, BaseMongoRepository


@dataclass
class MongoMessageRepository(BaseMongoRepository, BaseMessageRepository):

    async def save_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={
                "$push": {
                    "messages": converte_message2json(message),
                },
            },
        )

    async def get_messages_by_chat_oid(self, chat_oid: str) -> list[Message]:
        query_filter = {"oid": chat_oid}
        return await self._collection.find_one(query_filter)["messages"]
