from dataclasses import dataclass, field
from abc import ABC
from datetime import datetime
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
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
