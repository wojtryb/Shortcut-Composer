# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel

from ..label_widget_style import LabelWidgetStyle
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface

T = TypeVar("T", bound=LabelInterface)


class IconLabelWidget(LabelWidget[T]):
    """Displays a `label` which holds an icon."""

    def __init__(
        self,
        label: T,
        label_widget_style: LabelWidgetStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(label, label_widget_style, parent)
        self._pyqt_label = self._create_pyqt_label()

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, QIcon):
            raise TypeError("Label supposed to be QIcon.")

        size = round(self.icon_radius*1.1)

        label = QLabel(self)
        label.setScaledContents(False)
        label.setPixmap(to_display.pixmap(size, size))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.resize(size, size)
        label.move(self.center.x()-size//2, self.center.y()-size//2)
        label.show()
        return label
