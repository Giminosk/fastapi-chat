from dataclasses import dataclass

from domain.exceptions.message import (EmptyMessageException,
                                       TooLongMessageException)
from domain.values.base import BaseValue


@dataclass(frozen=True)
class Text(BaseValue):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyMessageException()
        if len(self.value) > 1000:
            raise TooLongMessageException()

    def as_generic_type(self) -> str:
        return str(self.value)
