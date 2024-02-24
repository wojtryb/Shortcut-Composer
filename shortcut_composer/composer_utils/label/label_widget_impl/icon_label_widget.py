# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QPixmap, QIcon

from api_krita.pyqt import PixmapTransform
from .image_label_widget import ImageLabelWidget


class IconLabelWidget(ImageLabelWidget):
    """Displays a `label` which holds an icon."""

    def _prepare_image(self) -> QPixmap:
        """Return icon after scaling it to fix QT_SCALE_FACTOR."""
        to_display = self.label.display_value

        if not isinstance(to_display, QIcon):
            raise TypeError("Label supposed to be QIcon.")

        size = round(self.icon_radius*1.1)
        return PixmapTransform.scale_pixmap(
            pixmap=to_display.pixmap(size, size),
            size_px=size)
