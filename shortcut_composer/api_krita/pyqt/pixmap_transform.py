# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QBrush,
)


class PixmapTransform:
    """Utilities for `QPixmap` transformation."""

    @staticmethod
    def add_border(pixmap: QPixmap, border_px: int) -> QPixmap:
        """Add a transparent border of `border_px` pixels on each side."""
        original_size = pixmap.width()
        new_size = original_size + 2*border_px

        result = QPixmap(new_size, new_size)
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(QPoint(), result)
        painter.drawPixmap(border_px, border_px, pixmap)
        painter.end()
        return result

    @staticmethod
    def make_pixmap_round(pixmap: QPixmap) -> QPixmap:
        """Make corners of the pixmap transparent, to make image a circle."""
        image = pixmap.toImage()
        image.convertToFormat(QImage.Format_ARGB32)

        imgsize = min(image.width(), image.height())
        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        painter = QPainter(out_img)
        painter.setBrush(QBrush(image))
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(0, 0, imgsize, imgsize)
        painter.end()

        return QPixmap.fromImage(out_img)

    @staticmethod
    def scale_pixmap(pixmap: QPixmap, size_px: int) -> QPixmap:
        """Scale a square pixmal to new size."""
        return pixmap.scaled(
            size_px,
            size_px,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
