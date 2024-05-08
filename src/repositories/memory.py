from dataclasses import dataclass, field

from domain.entities.chat import Chat
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
    
    async def delete_chat_by_title(self, title: str) -> None:
        self.chats = [chat for chat in self.chats if chat.title.as_generic_type() == title]