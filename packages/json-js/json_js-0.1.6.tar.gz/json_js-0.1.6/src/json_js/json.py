import keyword
from abc import ABC, abstractmethod
from typing import Any, MutableMapping, KeysView


class JSON(ABC):
    @abstractmethod
    def __new__(cls, obj) -> Any:
        return super().__new__(cls)

    def __init__(self, data: MutableMapping[str, Any]) -> None:
        self.__data = {}
        for key, value in data.items():
            if keyword.iskeyword(key):
                key += "_"
            self.__data[key] = value

    @abstractmethod
    def __getattr__(self, name) -> Any:
        pass

    def __dir__(self) -> KeysView[Any]:
        return self.__data.keys()

    def __repr__(self) -> str:
        return f"<JSON({self.__data!r}>)"
