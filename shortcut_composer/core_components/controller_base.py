from typing import Any


class Controller:
    """Component that allows to get and set a specific property of krita."""

    default_value: Any = None

    def refresh(self) -> None: """Refresh stored krita components."""
    def get_value(self) -> Any: """Get handled value from krita."""
    def set_value(self, value: Any) -> None: """Set handled value in krita."""
