from PyQt5.QtWidgets import QWidget

from .timer import Timer


class AnimatedWidget(QWidget):
    """Adds the fade-in animation when the widget is shown (60 FPS)."""

    def __init__(self, parent, animation_time: float = 0) -> None:
        super().__init__(parent)
        self._animation_time = animation_time
        self._animation_interval = self._read_animation_interval()
        self._animation_timer = Timer(self._increase_opacity, 17)

    def _increase_opacity(self):
        """Add interval to current opacity, stop the timer when full."""
        current_opacity = self.windowOpacity()
        self.setWindowOpacity(current_opacity+self._animation_interval)
        if current_opacity >= 1:
            self._animation_timer.stop()

    def show(self):
        """Decrease opacity to 0, and start a timer which animates it."""
        self.setWindowOpacity(0)
        self._animation_timer.start()
        super().show()

    def _read_animation_interval(self):
        """Return how much opacity (0-1) should be increased on each frame."""
        if time := self._animation_time:
            return 0.0167/time
        return 1
