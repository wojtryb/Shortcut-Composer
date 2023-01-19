# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.pyqt import Text
from typing import Union, Any
from dataclasses import dataclass

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import (
    QPixmap,
    QIcon,
)

from composer_utils import Config


@dataclass
class Label:
    """
    Data representing a single value in PieWidget.

    - `value` -- Value to set using the controller
    - `center -- Label position in widget coordinates
    - `angle` -- Angle in degrees in relation to widget center. Angles are
                 counted clockwise with 0 being the top of widget
    - `display_value` -- `value` representation to display. Can be
                         either a colored text or an image
    """

    value: Any
    center: QPoint = QPoint(0, 0)
    angle: int = 0
    display_value: Union[QPixmap, QIcon, Text, None] = None

    def __post_init__(self):
        self.activation_progress = AnimationProgress(speed_scale=1, steep=1)

    def swap_locations(self, other: 'Label'):
        self.angle, other.angle = other.angle, self.angle
        self.center, other.center = other.center, self.center


class AnimationProgress:
    """
    Grants interface to track progress of two-way steep animation.

    Holds the state of animation as float in range <0-1> which can be
    obtained with `value` property.

    Animation state can be altered with `up()` and `down()` methods.
    The change is the fastest when the animation starts, and then slows
    down near the end (controlled by `steep` argument)
    """

    def __init__(self, speed_scale: float = 1.0, steep: float = 1.0) -> None:
        self._value = 0
        self._speed = 0.004*Config.get_sleep_time()*speed_scale
        self._steep = steep

    def up(self):
        """Increase the animation progress."""
        difference = (1+self._steep-self._value) * self._speed
        self._value = min(self._value + difference, 1)

    def down(self):
        """Decrease the animation progress."""
        difference = (self._value+self._steep) * self._speed
        self._value = max(self._value - difference, 0)

    @property
    def value(self):
        """Get current state of animation. Is in range <0-1>."""
        return self._value

    def set(self, value: float):
        """Arbitralily set a value"""
        self._value = value
