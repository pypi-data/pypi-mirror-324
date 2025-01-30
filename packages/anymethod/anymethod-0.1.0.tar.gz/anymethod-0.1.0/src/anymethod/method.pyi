from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar('F', bound=Callable[..., Any])

class anymethod[F]:
    func: F
    def __init__(self, func: F) -> None: ...
    def __get__(self, obj: Any, cls: type | None = None) -> F: ...
    @property
    def __isabstractmethod__(self) -> bool: ...
