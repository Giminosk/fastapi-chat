from pydantic import BaseModel

from repositories.filters.message import GetMessagesFilters as GetMessagesInfraFilters


class GetMessagesFilters(BaseModel):
    offset: int = 0
    limit: int = 10

    def as_infra_filter(self):
        return GetMessagesInfraFilters(**self.model_dump())