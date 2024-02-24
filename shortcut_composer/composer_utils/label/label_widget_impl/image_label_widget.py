# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from api_krita.pyqt import Painter, PixmapTransform
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
        self.ready_image = self._prepare_image()

    def paint(self, painter: Painter) -> None:
        super().paint(painter)
        painter.paint_pixmap(self.center, self.ready_image)

    def _prepare_image(self) -> QPixmap:
        """Return image after scaling and reshaping it to circle."""
        to_display = self.label.display_value

        if not isinstance(to_display, QPixmap):
            raise TypeError("Label supposed to be QPixmap.")

        rounded_image = PixmapTransform.make_pixmap_round(to_display)
        return PixmapTransform.scale_pixmap(
            pixmap=rounded_image,
            size_px=round((
                self.icon_radius
                - self._label_widget_style.border_thickness
                - self._active_indicator_thickness)*2))
