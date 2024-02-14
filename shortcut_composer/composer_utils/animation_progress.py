# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .global_config import Config


class AnimationProgress:
    """
    Grants interface to track progress of two-way steep animation.

    Holds the state of animation as float in range <0-1> which can be
    obtained with `value` property.

    Animation state can be altered with `up()` and `down()` methods.
    The change is the fastest when the animation starts, and then slows
    down near the end (controlled by `steep` argument).

    There is a `reset()` method to cancel the animation immediately.
    """

    def __init__(self, speed_scale: float = 1.0, steep: float = 1.0) -> None:
        self._value = 0
        self._speed = 0.004*Config.get_sleep_time()*speed_scale
        self._steep = steep

    def up(self) -> None:
        """Increase the animation progress."""
        difference = (1+self._steep-self._value) * self._speed
        self._value = min(self._value + difference, 1)

    def down(self) -> None:
        """Decrease the animation progress."""
        difference = (self._value+self._steep) * self._speed
        self._value = max(self._value - difference, 0)

    @property
    def value(self) -> float:
        """Get current state of animation. It is in range <0-1>."""
        return self._value

    def reset(self) -> None:
        """Arbitrarily set a value to 0"""
        self._value = 0
