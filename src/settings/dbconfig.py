from pydantic import Field
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    mongo_uri: str = Field(alias="MONGO_URI")
    mongo_database: str = Field(default="chat_database", alias="MONGO_DATABASE")
    mongo_chat_collection: str = Field(
        default="chat_collection", alias="MONGO_COLLECTION"
    )
    mongo_message_collection: str = Field(
        default="message_collection", alias="MONGO_MESSAGE_COLLECTION"
    )
