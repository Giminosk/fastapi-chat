from dataclasses import dataclass, field

from domain.entities.chat import Chat
from domain.entities.message import Message
from repositories.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def save_chat(self, chat: Chat) -> None:
        self.chats.append(chat)

    async def get_chat_by_title(self, title: str) -> Chat | None:
        for chat in self.chats:
            if chat.title.as_generic_type() == title:
                return chat
        return None

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        for chat in self.chats:
            if chat.oid == oid:
                return chat
        return None

    async def delete_chat_by_title(self, title: str) -> None:
        self.chats = [
            chat for chat in self.chats if chat.title.as_generic_type() == title
        ]

    async def save_message(self, chat_oid: str, message: Message) -> None:
        for i in range(len(self.chats)):
            if self.chats[i].oid == chat_oid:
                self.chats[i].add_message(message)
                break
