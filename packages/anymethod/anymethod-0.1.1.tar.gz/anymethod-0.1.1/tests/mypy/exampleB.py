from typing import Any, ClassVar
from anymethod import anymethod


class FooBar:
    _cls: ClassVar[list[Any]] = []
    _obj: list[Any]

    def __init__(self) -> None:
        self._obj = []

    @anymethod
    def add_value(owner, v: Any) -> None:
        if isinstance(owner, type):
            owner._cls.append(v)
        else:
            owner._obj.append(v)
