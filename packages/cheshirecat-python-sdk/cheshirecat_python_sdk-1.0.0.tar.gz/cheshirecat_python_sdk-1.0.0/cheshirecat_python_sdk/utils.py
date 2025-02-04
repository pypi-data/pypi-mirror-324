from typing import Dict, Type, TypeVar


T = TypeVar("T")


def deserialize(data: Dict, cls: Type[T]) -> T:
    return cls(**data)
