import abc
from typing import Generic, TypeVar

from ephemerista import BaseModel

T = TypeVar("T")


class Analysis(BaseModel, Generic[T], abc.ABC):
    def __init__(self, **data):
        super().__init__(**data)

    @abc.abstractmethod
    def analyze(self, **kwargs) -> T:
        raise NotImplementedError()
