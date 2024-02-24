# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, Literal

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMdiArea

EventCallback = Callable[[QEvent], None]


class ReleaseKeyEventFilter(QMdiArea):
    """Event filter for running registered callbacks on KeyRelease."""

    def __init__(self) -> None:
        """Create list to hold callbacks as they get registered."""
        super().__init__(None)
        self._release_callbacks: list[EventCallback] = []

    def register_release_callback(self, callback: EventCallback) -> None:
        """Register callback, so it can get executed on each KeyRelease."""
        self._release_callbacks.append(callback)

    def eventFilter(self, _, event: QEvent) -> Literal[False]:
        """
        Override filtering method, executed by Qt on every event.

        When the event is recognized to be KeyRelease event, run all
        registered callbacks.

        Always return False to let the event reach its desired
        destination.
        """
        if event.type() == QEvent.KeyRelease:
            for callback in self._release_callbacks:
                callback(event)

        return False
