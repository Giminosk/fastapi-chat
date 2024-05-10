from domain.entities.chat import Chat
from domain.entities.message import Message


def converte_message2json(message: Message) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
    }


def converte_chat2json(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "messages": [converte_message2json(message) for message in chat.messages],
    }
