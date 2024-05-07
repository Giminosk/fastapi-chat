from dataclasses import dataclass

from domain.exceptions.chat import EmptyTitleException, TooLongTitleException, TitleStrartsWithNoCapital
from domain.values.base import BaseValue


@dataclass(frozen=True)
class Title(BaseValue):
    value: str

    def validate(self) -> None:
        if not self.value:
            raise EmptyTitleException()
        if len(self.value) > 100:
            raise TooLongTitleException()
        if not self.value[0].isupper():
            raise TitleStrartsWithNoCapital()

    def as_generic_type(self) -> str:
        return str(self.value)
