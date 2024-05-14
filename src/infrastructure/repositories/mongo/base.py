from abc import ABC
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient


@dataclass
class BaseMongoRepository(ABC):
    client: AsyncIOMotorClient
    database: str
    collection_name: str

    @property
    def _collection(self):
        return self.client[self.database][self.collection_name]
