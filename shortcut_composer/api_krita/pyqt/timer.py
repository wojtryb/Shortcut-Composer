# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtCore import QTimer

EmptyCallback = Callable[[], None]


class Timer:
    """Wraps PyQt5 QTimer to simplify init interface."""

    def __init__(self, target: EmptyCallback, interval_ms: int) -> None:
        self._timer = QTimer()
        self._timer.timeout.connect(target)
        self._interval_ms = interval_ms

    def start(self) -> None:
        """Start a timer."""
        self._timer.start(self._interval_ms)

    def stop(self) -> None:
        """Stop a timer."""
        self._timer.stop()
