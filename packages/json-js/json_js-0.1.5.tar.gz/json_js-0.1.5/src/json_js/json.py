from abc import ABC, abstractmethod
from typing import Any, MutableMapping, KeysView


class JSON(ABC):
    def __init__(self, data: MutableMapping[Any, Any]) -> None:
        self.__data = data

    @abstractmethod
    def __getattr__(self, name) -> Any:
        pass

    def __dir__(self) -> KeysView[Any]:
        return self.__data.keys()

    def __repr__(self) -> str:
        return f"JSON({self.__data})"

    @classmethod
    @abstractmethod
    def build(cls, obj) -> Any:
        pass
