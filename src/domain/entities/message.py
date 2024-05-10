from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.message import Text


@dataclass(eq=False)
class Message(BaseEntity):
    text: Text
    chat_oid: str
