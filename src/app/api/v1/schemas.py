from typing import Generic, TypeVar

from pydantic import BaseModel

R = TypeVar("R")


class BaseQueryResponseSchema(BaseModel, Generic[R]):
    count: int
    offset: int
    limit: int
    results: R
