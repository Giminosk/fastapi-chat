from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
