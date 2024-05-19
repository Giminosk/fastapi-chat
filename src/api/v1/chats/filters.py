from pydantic import BaseModel

from infrastructure.repositories.filters.chat import (
    GetChatsFilters as GetChatsInfraFilters,
)
from infrastructure.repositories.filters.message import (
    GetMessagesFilters as GetMessagesInfraFilters,
)


class GetMessagesFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def as_infra_filter(self):
        return GetMessagesInfraFilters(**self.model_dump())


class GetChatsFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def as_infra_filter(self):
        return GetChatsInfraFilters(**self.model_dump())
