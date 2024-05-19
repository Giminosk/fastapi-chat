from dataclasses import dataclass


@dataclass
class GetChatsFilters:
    offset: int = 0
    limit: int = 10
