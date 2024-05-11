from dataclasses import dataclass


@dataclass
class GetMessagesFilters:
    offset: int = 0
    limit: int = 10
