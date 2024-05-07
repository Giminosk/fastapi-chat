from dataclasses import dataclass

from domain.exceptions.base import BaseAppException


@dataclass(eq=False)
class LogicException(BaseAppException):
    def __init__(self):
        super().__init__("Error occured while processing request")