from typing import Any, MutableMapping, override, MutableSequence

from .json import JSON

class FrozenJSON(JSON):
    def __new__(cls, obj) -> Any:
        if isinstance(obj, MutableMapping):
            return super().__new__(cls, obj)
        elif isinstance(obj, MutableSequence):
            return [cls(item) for item in obj]
        else:
            return obj

    def __init__(self, data: MutableMapping[Any, Any]) -> None:
        super().__init__(data)

    def __getattr__(self, name) -> Any:
        try:
            return getattr(self._JSON__data, name)
        except AttributeError:
            return FrozenJSON(self._JSON__data[name])

    @override
    def __repr__(self) -> str:
        return f"<FrozenJSON({self._JSON__data!r}>)"
