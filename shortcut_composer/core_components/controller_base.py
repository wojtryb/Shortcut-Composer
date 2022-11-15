from typing import TypeVar, Optional

T = TypeVar('T')


class Controller:
    """Component that allows to get and set a specific property of krita."""

    default_value: Optional[T] = None

    def refresh(self) -> None: ...
    def get_value(self) -> T: ...
    def set_value(self, value: T) -> None: ...
