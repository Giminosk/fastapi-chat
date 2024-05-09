from pydantic import BaseModel


class CreateChatRequestHandler(BaseModel):
    title: str


class CreateChatResponseHandler(BaseModel):
    chat_oid: str
    title: str
