from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic


T = TypeVar("T", bound=Any)


@dataclass(frozen=True)
class BaseValue(ABC, Generic[T]):
    value: T

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        pass

    @abstractmethod
    def as_generic_type(self) -> T:
        pass
