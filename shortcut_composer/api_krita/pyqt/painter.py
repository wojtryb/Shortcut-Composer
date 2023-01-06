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

    def paint_pie(self, center: QPoint, angle: int, span: int, color: QColor):
        path = QPainterPath()
        path.moveTo(center)
        start = 10
        length = 45
        radius = 50
        rectangle = QRectF(center.x()-radius, center.y()-radius, radius*2, radius*2)
        path.arcTo(rectangle, start, length)

        radius = 25
        rectangle = QRectF(center.x()-radius, center.y()-radius, radius*2, radius*2)
        path.arcTo(rectangle, start+length, -length)

        self._painter.fillPath(path, color)

    def end(self):
        self._painter.end()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.end()
