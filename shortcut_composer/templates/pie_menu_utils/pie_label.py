# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Final
from dataclasses import dataclass, field

try:
    from PyQt5.QtCore import QPoint
    from PyQt5.QtGui import QPixmap, QIcon
except ModuleNotFoundError:
    from PyQt6.QtCore import QPoint
    from PyQt6.QtGui import QPixmap, QIcon

from composer_utils import AnimationProgress
from composer_utils.label import LabelInterface, LabelText
from core_components import Controller

T = TypeVar("T")


@dataclass
class PieLabel(LabelInterface, Generic[T]):
    """
    Data representing a single value in PieWidget.

    - `value`         -- value to set using the controller
    - `display_value` -- `value` representation to display. Can be
                         a colored text, image or an icon
    - `pretty_name`   -- full name of value
    - `center         -- position of center in PieWidget coordinates
    - `angle`         -- Angle [°] in relation to widget center. Angles
                         are counted clockwise with 0 being widget top
    - `activation_progress` -- state of animation in range <0-1>
    """

    value: Final[T]
    display_value: QPixmap | QIcon | LabelText | None = None
    pretty_name: str = ""
    center: QPoint = field(default_factory=QPoint)
    angle: int = 0
    activation_progress: AnimationProgress = field(
        default_factory=AnimationProgress)

    def __eq__(self, other: T) -> bool:
        """Consider two labels with the same value equal."""
        if not isinstance(other, PieLabel):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Use value for hashing, as it should not change over time."""
        return hash(self.value)

    @staticmethod
    def from_value(value: T, controller: Controller) -> 'PieLabel[T] | None':
        """Use controller to create a label holding passed value."""
        label = controller.get_label(value)
        if label is None:
            return None

        return PieLabel(
            value=value,
            display_value=label,
            pretty_name=controller.get_pretty_name(value))
