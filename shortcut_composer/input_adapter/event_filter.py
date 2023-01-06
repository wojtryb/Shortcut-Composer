from typing import Callable, List, Literal

from PyQt5.QtCore import QEvent

from api_krita import QMdiArea  # type: ignore

EventCallback = Callable[[QEvent], None]


class ReleaseKeyEventFilter(QMdiArea):
    """Event filter for running registered callbacks on KeyRelease."""

    def __init__(self):
        """Create list to hold callbacks as they get registered."""
        super().__init__(None)
        self._release_callbacks: List[EventCallback] = []

    def register_release_callback(self, callback: EventCallback) -> None:
        """Register callback, so it can get executed on each KeyRelease."""
        self._release_callbacks.append(callback)

    def eventFilter(self, _, event: QEvent) -> Literal[False]:
        """
        Override filtering method, executed by Qt on every event.

        When the event is recognised to be KeyRelease event, run all
        registered callbacks.

        Always return False to let the event reach its desired
        destination.
        """
        if event.type() == QEvent.KeyRelease:
            for callback in self._release_callbacks:
                callback(event)

        return False