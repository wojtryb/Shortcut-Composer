from typing import Callable

from PyQt5.QtCore import QTimer

EmptyCallback = Callable[[], None]

class Timer:
    """Wraps PyQt5 QTimer to simplify init interface."""

    def __init__(self, target: EmptyCallback, time_ms: int) -> None:
        self._timer = QTimer()
        self._timer.timeout.connect(target)
        self._time_ms = time_ms
    
    def start(self):
        """Start a timer."""
        self._timer.start(self._time_ms)

    def stop(self):
        """Stop a timer."""
        self._timer.stop()