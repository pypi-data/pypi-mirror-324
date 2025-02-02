from typing import Any, MutableMapping, override

from .json import JSON

class FrozenJSON(JSON):
    def __init__(self, data: MutableMapping[Any, Any]) -> None:
        super().__init__(data)

    def __getattr__(self, name) -> Any:
        pass

    @override
    def __repr__(self) -> str:
        return f"FrozenJSON({self._JSON__data})"

    @classmethod
    def build(cls, obj) -> Any:
        pass
