from domain.entities.chat import Chat
from domain.entities.message import Message


def converter_message2json(message: Message) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
    }


def converter_chat2json(chat: Chat) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "messages": [converter_message2json(message) for message in chat.messages],
    }
