# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QPixmap
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

    def paint(self, painter: Painter):
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
            size_px=round((self.icon_radius-self._thickness)*2))
