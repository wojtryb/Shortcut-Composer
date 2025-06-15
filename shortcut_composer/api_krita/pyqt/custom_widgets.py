# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
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
        return self.pos() + self.center

    def move_center(self, new_center: QPoint) -> None:
        """Move the widget by providing a new center point."""
        self.move(new_center-self.center)


class AnimatedWidget(QWidget):
    """Adds the fade-in animation when the widget is shown."""

    def __init__(
        self,
        animation_time_s: float = 0,
        fps_limit: int = 60,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._animation_duration = animation_time_s
        self._check_interval_ms = round(1000 / fps_limit)
        self._opacity_change = self._read_animation_interval()
        self._timer = Timer(self._increase_opacity, self._check_interval_ms)

    def show(self) -> None:
        """Decrease opacity to 0, and start a timer which animates it."""
        self.setWindowOpacity(0)
        self._timer.start()
        super().show()

    def _increase_opacity(self) -> None:
        """Add interval to current opacity, stop the timer when full."""
        current_opacity = self.windowOpacity()
        self.setWindowOpacity(current_opacity+self._opacity_change)
        self.repaint()
        if current_opacity >= 1:
            self._timer.stop()

    def _read_animation_interval(self) -> float:
        """Return how much opacity (0-1) should be increased on each frame."""
        if self._animation_duration:
            return 0.001 * self._check_interval_ms / self._animation_duration
        return 1
