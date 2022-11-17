from typing import Any


class Controller:
    """Component that allows to get and set a specific property of krita."""

    default_value: Any = None

    def refresh(self) -> None: ...
    def get_value(self) -> Any: ...
    def set_value(self, value: Any) -> None: ...
