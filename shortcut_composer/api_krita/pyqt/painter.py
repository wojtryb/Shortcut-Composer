from typing import Optional

from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint, QRectF


class Painter:
    def __init__(self, widget: QWidget, event) -> None:
        self._painter = QPainter(widget)
        self._painter.eraseRect(event.rect())
        self._painter.setRenderHints(QPainter.Antialiasing)

    def paint_wheel(
        self,
        center: QPoint,
        outer_radius: float,
        color: QColor,
        thickness: Optional[float] = None,
    ):
        path = QPainterPath()
        path.addEllipse(center, outer_radius, outer_radius)
        if thickness:
            inner_radius = outer_radius - thickness
            path.addEllipse(center, inner_radius, inner_radius)
        self._painter.fillPath(path, color)

    def paint_pixmap(self, center: QPoint, pixmap: QPixmap):
        left_top_corner = QPoint(
            center.x() - pixmap.width()//2,
            center.y() - pixmap.height()//2
        )
        self._painter.drawPixmap(left_top_corner, pixmap)

    def paint_pie(
        self,
        center: QPoint,
        outer_radius: int,
        angle: int,
        span: int,
        color: QColor,
        thickness: Optional[float] = None,
    ):
        angle = -angle + 90
        path = QPainterPath()
        path.moveTo(center)
        rectangle = QRectF(
            center.x()-outer_radius,
            center.y()-outer_radius,
            outer_radius*2,
            outer_radius*2
        )
        path.arcTo(rectangle, angle-span//2, span)

        if thickness:
            inner_radius = outer_radius-thickness
            rectangle = QRectF(
                center.x()-inner_radius,
                center.y()-inner_radius,
                inner_radius*2,
                inner_radius*2
            )
            path.arcTo(rectangle, angle+span//2, -span)

        self._painter.fillPath(path, color)

    def end(self):
        self._painter.end()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.end()
