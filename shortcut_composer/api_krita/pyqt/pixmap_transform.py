# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import (
        QPainter,
        QPixmap,
        QImage,
        QBrush)
except ModuleNotFoundError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import (
        QPainter,
        QPixmap,
        QImage,
        QBrush)


class PixmapTransform:
    """Utilities for `QPixmap` transformation."""

    @staticmethod
    def make_pixmap_round(pixmap: QPixmap) -> QPixmap:
        """Make corners of the pixmap transparent, to make image a circle."""
        image = pixmap.toImage()
        image.convertToFormat(QImage.Format.Format_ARGB32)

        img_size = min(image.width(), image.height())
        out_img = QImage(img_size, img_size, QImage.Format.Format_ARGB32)
        out_img.fill(Qt.GlobalColor.transparent)

        painter = QPainter(out_img)
        painter.setBrush(QBrush(image))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.drawEllipse(0, 0, img_size, img_size)
        painter.end()

        return QPixmap.fromImage(out_img)

    @staticmethod
    def scale_pixmap(pixmap: QPixmap, size_px: int) -> QPixmap:
        """Scale a square pixmap to new size."""
        return pixmap.scaled(
            size_px,
            size_px,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
