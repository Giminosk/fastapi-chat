from dataclasses import dataclass, field
from abc import ABC
import datetime
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    oid: int = field(
        default_factory=uuid4(),
        kw_only=True,
    )
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.oid)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, BaseEntity):
            return self.oid == other.oid
        return False
    