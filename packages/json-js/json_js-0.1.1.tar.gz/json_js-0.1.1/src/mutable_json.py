from typing import Any, override

from src.json import JSON

class MutableJSON(JSON):
    def __init__(self, data) -> None:
        super().__init__(data)

    def __getattr__(self, name) -> Any:
        pass

    @override
    def __repr__(self) -> str:
        return f"MutableJSON({self._JSON__data})"

    @classmethod
    def build(cls, obj) -> Any:
        pass
