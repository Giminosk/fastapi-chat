from pydantic import BaseModel


class CreateChatRequestHandler(BaseModel):
    title: str


class CreateChatResponseHandler(BaseModel):
    chat_oid: str
    title: str


class CreateMessageRequestHandler(BaseModel):
    text: str


class CreateMessageResponseHandler(BaseModel):
    chat_oid: str
    message_oid: str
    text: str
