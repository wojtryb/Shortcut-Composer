# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math

from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPixmap, QPaintEvent
from PyQt5.QtCore import QPoint, QRectF
from PyQt5.QtWidgets import QWidget


class Painter:
    """
    Wraps `QPainter` to extend it with custom shapes to paint.

    Allows to paint:
    - wheel of given thickness, color and radius
    - pie being a part of a wheel
    - pixmap providing a center instead of top-left corner

    Unlike original painter, can be used with context manager.
    """

    def __init__(self, widget: QWidget, event: QPaintEvent) -> None:
        self._painter = QPainter(widget)
        self._painter.eraseRect(event.rect())
        self._painter.setRenderHints(QPainter.Antialiasing)

    def paint_wheel(
        self,
        center: QPoint,
        outer_radius: float,
        color: QColor,
        thickness: float | None = None,
    ) -> None:
        """
        Paint a wheel at center providing its radius, color and thickness.

        Not providing thickness results in fully filled circle.
        """
        path = QPainterPath()
        path.addEllipse(center, outer_radius, outer_radius)
        if thickness:
            inner_radius = outer_radius - thickness
            path.addEllipse(center, inner_radius, inner_radius)
        self._painter.fillPath(path, color)

    def paint_pie(
        self,
        center: QPoint,
        outer_radius: int,
        angle: int,
        span: int,
        color: QColor,
        thickness: float | None = None,
    ) -> None:
        """Paint part of wheel a, that spans left and right by span/2."""
        angle = -angle + 90
        path = QPainterPath()
        path.moveTo(center)
        outer_rectangle = self._square(center, outer_radius*2)
        path.arcTo(outer_rectangle, angle-math.floor(span/2), span)

        if thickness:
            inner_radius = outer_radius-thickness
            inner_rectangle = self._square(center, round(inner_radius*2))
            path.arcTo(inner_rectangle, angle+math.ceil(span/2), -span)

        self._painter.fillPath(path, color)

    def paint_pixmap(self, center: QPoint, pixmap: QPixmap) -> None:
        """Paint pixmap providing a center instead of top-left corner."""
        self._painter.drawPixmap(
            center.x() - pixmap.width()//2,
            center.y() - pixmap.height()//2,
            pixmap.width(),
            pixmap.height(),
            pixmap)

    def _square(self, center: QPoint, width: int) -> QRectF:
        """Return a square of given `width` at `center` point."""
        return QRectF(center.x()-width//2, center.y()-width//2, width, width)

    def end(self) -> None:
        """End painting a widget provided in __init__."""
        self._painter.end()

    def __enter__(self) -> 'Painter':
        """Start using a painter using context manager."""
        return self

    def __exit__(self, *_) -> None:
        """End using a painter using context manager."""
        self.end()
