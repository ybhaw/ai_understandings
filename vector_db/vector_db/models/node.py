from typing import Generic, TypeVar
import uuid

T = TypeVar("T")


class Node(Generic[T]):
    vector: list[float]
    data: T
    uuid: uuid.uuid4
