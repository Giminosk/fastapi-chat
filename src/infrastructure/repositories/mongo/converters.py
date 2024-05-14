from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.chat import Title
from domain.values.message import Text


def converte_message2json(message: Message) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
        "created_at": message.created_at,
        "chat_oid": message.chat_oid,
    }


def converte_json2message(message: dict) -> Message:
    return Message(
        oid=message["oid"],
        text=Text(value=message["text"]),
        chat_oid=message["chat_oid"],
        created_at=message["created_at"],
    )


def converte_chat2json(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
    }


def converte_json2chat(chat: dict) -> Chat:
    return Chat(
        oid=chat["oid"],
        title=Title(value=chat["title"]),
        created_at=chat["created_at"],
    )
