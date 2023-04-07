# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import (
    QPixmap,
    QPaintEvent,
)
from PyQt5.QtWidgets import QWidget

from api_krita.pyqt import Painter, PixmapTransform
from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget


class ImageLabelWidget(LabelWidget):
    """Displays a `label` which holds an image."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
        is_unscaled: bool = False,
    ) -> None:
        super().__init__(label, style, parent, is_unscaled)
        self.ready_image = self._prepare_image()

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the entire widget using the Painter wrapper.

        Paint a background behind a label its border, and image itself.
        """
        with Painter(self, event) as painter:
            painter.paint_wheel(
                center=self.center,
                outer_radius=self.icon_radius,
                color=self._style.icon_color)

            painter.paint_wheel(
                center=self.center,
                outer_radius=(
                    self.icon_radius-self._style.border_thickness//2),
                color=self._border_color,
                thickness=self._style.border_thickness)
            painter.paint_pixmap(self.center, self.ready_image)

    def _prepare_image(self) -> QPixmap:
        """Return image after scaling and reshaping it to circle."""
        to_display = self.label.display_value

        if not isinstance(to_display, QPixmap):
            raise TypeError("Label supposed to be QPixmap.")

        rounded_image = PixmapTransform.make_pixmap_round(to_display)
        return PixmapTransform.scale_pixmap(
            pixmap=rounded_image,
            size_px=round(self.icon_radius*1.8))
