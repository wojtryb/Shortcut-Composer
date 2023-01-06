from typing import Callable, List

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QKeyEvent
from ..api import QMdiArea

EventCallback = Callable[[QEvent], None]


class ReleaseKeyEventFilter(QMdiArea):
    """Event filter that runs all registered callbacks on every KeyRelease."""

    def __init__(self):
        """Create list for callbacks that gets registered."""
        super().__init__(None)
        self._release_callbacks: List[EventCallback] = []

    def register_release_callback(self, callback: EventCallback) -> None:
        """Add new callback to list, so it gets executed on each KeyRelease."""
        self._release_callbacks.append(callback)

    def eventFilter(self, _, event: QKeyEvent) -> bool:
        """Everrides QMdiArea method - executed on every krita event."""
        if event.type() == QEvent.KeyRelease:
            for callback in self._release_callbacks:
                callback(event)

        return False
