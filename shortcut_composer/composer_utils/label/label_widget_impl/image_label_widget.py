# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from api_krita.pyqt import PixmapTransform
from ..label_widget_style import LabelWidgetStyle
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface

T = TypeVar("T", bound=LabelInterface)


class ImageLabelWidget(LabelWidget[T]):
    """Displays a `label` which holds an image."""

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

        if not isinstance(to_display, QPixmap):
            raise TypeError("Label supposed to be QPixmap.")

        size = round((
            self.icon_radius
            - self._label_widget_style.border_thickness
            - self._active_indicator_thickness)*2)

        label = QLabel(self)
        label.setScaledContents(True)
        label.setPixmap(PixmapTransform.make_pixmap_round(to_display))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.resize(size, size)
        label.move(self.center.x()-size//2, self.center.y()-size//2)
        label.show()
        return label
