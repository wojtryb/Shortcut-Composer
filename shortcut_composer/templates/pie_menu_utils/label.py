# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Any
from dataclasses import dataclass

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import (
    QPixmap,
    QIcon,
)

from api_krita.pyqt import Text
from .animation_progress import AnimationProgress


@dataclass
class Label:
    """
    Paintable representation of value in PieWidget.

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
