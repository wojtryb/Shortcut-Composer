# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

try:
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtGui import QColor
except ModuleNotFoundError:
    from PyQt6.QtWidgets import QWidget
    from PyQt6.QtGui import QColor

from api_krita.pyqt import Painter
from ..label_widget_style import LabelWidgetStyle
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface

T = TypeVar("T", bound=LabelInterface)


class QColorLabelWidget(LabelWidget[T]):
    """Displays a `label` which holds a color."""

    def __init__(
        self,
        label: T,
        label_widget_style: LabelWidgetStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(label, label_widget_style, parent)

    def paint(self, painter: Painter) -> None:
        """Fill entire background with held color."""
        super().paint(painter)

        if not isinstance(self.label.display_value, QColor):
            raise ValueError

        painter.paint_wheel(
            center=self.center,
            outer_radius=(
                self.icon_radius
                - self._active_indicator_thickness
                - self._label_widget_style.border_thickness//2),
            color=self.label.display_value)
