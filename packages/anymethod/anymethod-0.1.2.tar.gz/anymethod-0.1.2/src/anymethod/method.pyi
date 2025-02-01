from collections.abc import Callable
from typing import Any, Concatenate, Generic, ParamSpec, TypeVar

O = TypeVar('O')
P = ParamSpec('P')
R = TypeVar('R', covariant=True)

class anymethod(Generic[O, P, R]):
    func: Callable[Concatenate[O, P], R]
    def __init__(self, func: Callable[Concatenate[O, P], R]) -> None: ...
    def __get__(self, obj: Any, cls: Any) -> Callable[P, R]: ...
    @property
    def __isabstractmethod__(self) -> bool: ...
