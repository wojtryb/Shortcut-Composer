# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Final
from dataclasses import dataclass, field

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QIcon

from composer_utils import AnimationProgress
from composer_utils.label import LabelInterface, LabelText
from core_components import Controller

T = TypeVar("T")


@dataclass
class PieLabel(LabelInterface, Generic[T]):
    """
    Data representing a single value in PieWidget.

    - `value` -- Value to set using the controller
    - `display_value` -- `value` representation to display. Can be
                         either a colored text or an image
    - `pretty_name` -- String to use when displaying the label to user
    - `center -- Label position in widget coordinates
    - `angle` -- Angle in degrees in relation to widget center. Angles are
                 counted clockwise with 0 being the top of widget
    - `activation_progress` -- state of animation in range <0-1>
    """

    value: Final[T]
    display_value: QPixmap | QIcon | LabelText | None = None
    pretty_name: str = ""
    center: QPoint = field(default_factory=QPoint)
    angle: int = 0

    def __post_init__(self) -> None:
        self.activation_progress = AnimationProgress(speed_scale=1, steep=1)

    def swap_locations(self, other: 'PieLabel[T]') -> None:
        """Change position data with information Label."""
        self.angle, other.angle = other.angle, self.angle
        self.center, other.center = other.center, self.center

    def __eq__(self, other: T) -> bool:
        """Consider two labels with the same value and position - equal."""
        if not isinstance(other, PieLabel):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        """Use value for hashing, as it should not change over time."""
        return hash(self.value)

    @staticmethod
    def from_value(value: T, controller: Controller)\
            -> 'PieLabel[T] | None':
        """Use provided controller to create a label holding passed value."""
        label = controller.get_label(value)
        if label is None:
            return None

        return PieLabel(
            value=value,
            display_value=label,
            pretty_name=controller.get_pretty_name(value))
