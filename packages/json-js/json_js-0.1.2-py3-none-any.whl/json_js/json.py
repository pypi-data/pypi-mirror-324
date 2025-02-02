from abc import ABC, abstractmethod
from typing import Any

class JSON(ABC):
    def __init__(self, data) -> None:
        self.__data = data

    @abstractmethod
    def __getattr__(self, name) -> Any:
        pass

    def __dir__(self):
        return self.__data.keys()

    def __repr__(self) -> str:
        return "JSON()"

    @classmethod
    @abstractmethod
    def build(cls, obj) -> Any:
        pass
