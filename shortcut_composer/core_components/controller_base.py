from abc import ABC, abstractmethod
from typing import Any


class Controller(ABC):
    """Component that allows to get and set a specific property of krita."""
    default_value: Any = None
    @abstractmethod
    def get_value(self) -> Any: ...
    @abstractmethod
    def set_value(self, value) -> None: ...
