from pydantic import Field
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    mongo_uri: str = Field(alias="MONGO_URI")
    mongo_database: str = Field(default="chat_database", alias="MONGO_DATABASE")
    mongo_collection: str = Field(default="chat_collection", alias="MONGO_COLLECTION")
