# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint

from .timer import Timer


class BaseWidget(QWidget):
    """Adds base convenience methods to the widget."""

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent)

    @property
    def center(self) -> QPoint:
        """Return point with center widget's point in its coordinates."""
        return QPoint(self.size().width()//2, self.size().height()//2)

    @property
    def center_global(self) -> QPoint:
        """Return point with center widget's point in screen coordinates."""
        return self.pos() + self.center  # type: ignore

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self.center)  # type: ignore


class AnimatedWidget(QWidget):
    """Adds the fade-in animation when the widget is shown (60 FPS)."""

    def __init__(self, parent, animation_time: float = 0) -> None:
        super().__init__(parent)
        self._animation_time = animation_time
        self._animation_interval = self._read_animation_interval()
        self._animation_timer = Timer(self._increase_opacity, 17)

    def show(self) -> None:
        """Decrease opacity to 0, and start a timer which animates it."""
        self.setWindowOpacity(0)
        self._animation_timer.start()
        super().show()

    def _increase_opacity(self) -> None:
        """Add interval to current opacity, stop the timer when full."""
        current_opacity = self.windowOpacity()
        self.setWindowOpacity(current_opacity+self._animation_interval)
        if current_opacity >= 1:
            self._animation_timer.stop()

    def _read_animation_interval(self) -> float:
        """Return how much opacity (0-1) should be increased on each frame."""
        if time := self._animation_time:
            return 0.0167/time
        return 1
