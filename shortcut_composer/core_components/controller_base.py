from abc import ABC, abstractmethod
from typing import TypeVar, Optional

T = TypeVar('T')


class Controller(ABC):
    """Component that allows to get and set a specific property of krita."""

    default_value: Optional[T] = None

    def refresh(self) -> None: ...
    @abstractmethod
    def get_value(self) -> T: ...
    @abstractmethod
    def set_value(self, value: T) -> None: ...
