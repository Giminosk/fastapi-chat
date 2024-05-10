from dataclasses import is_dataclass
from domain.entities.base import BaseEntity
from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.chat import Title
from domain.values.message import Text


def is_dataclass_instance(entity: BaseEntity | object):
    return is_dataclass(entity) and not isinstance(entity, type)


def converter(entity: BaseEntity | object) -> dict:
    if is_dataclass_instance(entity):
        result = {}
        for field_name in entity.__dataclass_fields__:
            if field_name != "events":
                value = getattr(entity, field_name)
                result[field_name] = converter(value)
        return result
    elif isinstance(entity, (list, tuple)):
        return [converter(item) for item in entity]
    elif isinstance(entity, dict):
        return {key: converter(value) for key, value in entity.items()}
    else:
        return entity
