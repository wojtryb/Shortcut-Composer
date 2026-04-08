# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable
from time import time_ns

from PyQt.QtWidgets import QWidget

from .timer import Timer


class AnimatedWidget(QWidget):
    """Adds the fade-in animation when the widget is shown."""

    def __init__(
        self,
        animation_time_s: float = 0,
        fps_limit: int = 60,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.animation_processor = AnimationProcessor(fps_limit)
        self.animation_processor.repaint_callback = self.repaint
        self._fade_in_animation = Animation(
            update_callback=self._update_opacity,
            duration_s_callback=lambda: animation_time_s)

    def _update_opacity(self, opacity: float):
        self.setWindowOpacity(opacity)
        self.repaint()

    def show(self) -> None:
        """Decrease opacity to 0, and start a timer which animates it."""
        self.setWindowOpacity(0)
        self._fade_in_animation.reset()
        self.animation_processor.add(
            animation=self._fade_in_animation,
            is_ascending=True)
        super().show()

    def hide(self) -> None:
        self.animation_processor.purge()
        super().hide()


class AnimationProcessor:
    """
    Handles multiple animations with a single timer.

    Call `add()` to start an animation, which will be updated at fixed
    intervals (`fps_limit`). The timer is stopped when all added
    animations were finished.

    It is recommended to add related QWidget's `paint` method as
    `repaint_callback`, so that it is called every time the animations
    are updated.
    """

    def __init__(self, fps_limit: int = 60) -> None:
        self._animations: list[Animation] = []
        self._check_interval_ms = round(1000/fps_limit) if fps_limit else 1
        self._timer = Timer(self._tick, self._check_interval_ms)
        self.repaint_callback = lambda: None

    def add(self, animation: 'Animation', is_ascending: bool) -> None:
        """Start new animation from its current state towards 1 or 0."""
        animation.start(is_ascending)

        if animation not in self._animations:
            self._animations.append(animation)

        self._timer.start()

    def purge(self) -> None:
        """Reset all running animation to 0 and stop them."""
        for animation in self._animations:
            animation.reset()
        self._animations.clear()

    def _tick(self):
        """Update all running animations, run repaint_callbaak afterwards."""
        if not self._animations:
            self._timer.stop()

        for animation in self._animations:
            status = animation.update()
            if status is True:
                self._animations.remove(animation)

        self.repaint_callback()


class Animation:
    """
    Manages animation of a single component/property.

    Call `start(is_ascending=True)` to start a animation. Then, calling
    `update()` will modify the internal state of the animation based on
    elapsed time.

    Getting the `value` property afterwards returns current state of the
    animation (being 0 at start and 1 at the end). Calling
    `start(is_ascending=True)` will cause the animation to run in
    reverse order towards 0. If the animation was still running at that
    time, it will start going down from its current state. 

    update() returns True when the animation is finished.

    It is possible to register a callback performing some operation on
    current `value` when `update()` is called. 
    """

    def __init__(
        self,
        update_callback: Callable[[float], None] = lambda _: None,
        duration_s_callback: Callable[[], float] = lambda: 0,
    ) -> None:
        self._update_callback = update_callback
        self._duration_s_cb = duration_s_callback

        # Static during animation
        self._start_time_ms = 0
        self._initial_value = 0
        self._duration_ms = 0
        self._is_ascending = False

        # Changes with time
        self._value = 0
        self._is_running = False

    def start(self, is_ascending: bool) -> None:
        """Start animation from current state towards 1 (is_ascending) or 0."""
        self._start_time_ms = 0.000_001 * time_ns()
        self._initial_value = self._value
        self._duration_ms = 1000 * self._duration_s_cb()
        self._is_ascending = is_ascending
        self._is_running = True

    def update(self) -> bool:
        """
        Update animation state based on time elapsed from last start call.

        Returns True when the animation is finished.
        """
        if not self._is_running:
            return True

        delta_ms = 0.000_001*time_ns() - self._start_time_ms
        d = delta_ms / self._duration_ms if self._duration_ms else float("inf")

        if self._is_ascending:
            self._value = self._initial_value + d
            self._value = min(1, self._value)
            self._update_callback(self._value)
            if self._value == 1:
                return True
        else:
            self._value = self._initial_value - d
            self._value = max(0, self._value)
            self._update_callback(self._value)
            if self._value == 0:
                return True

        return False

    def reset(self) -> None:
        """Reset Animation to the initial state of 0."""
        self._value = 0
        self._is_running = False

    @property
    def value(self) -> float:
        """Return current value of animation. Needs a update call()."""
        return self._value
