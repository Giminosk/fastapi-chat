from dataclasses import dataclass


@dataclass
class BaseAppException(Exception):
    @property
    def message(self):
        return "Application error occurred"
