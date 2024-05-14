import datetime

from pydantic import BaseModel

from api.v1.schemas import BaseQueryResponseSchema


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    chat_oid: str
    title: str


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    chat_oid: str
    message_oid: str
    text: str


class GetMessageSchema(BaseModel):
    message_oid: str
    text: str
    created_at: datetime.datetime
    chat_oid: str


class GetChatSchema(BaseModel):
    chat_oid: str
    title: str
    created_at: datetime.datetime


class GetMessagesResponseSchema(BaseQueryResponseSchema[list[GetMessageSchema]]):
    pass
