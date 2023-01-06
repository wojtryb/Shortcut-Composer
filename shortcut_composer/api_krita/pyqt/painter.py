from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint


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
        fill_part: float = 1.0,
    ):
        # fill : (0.0-1.0>
        path = QPainterPath()
        path.addEllipse(center, outer_radius, outer_radius)
        if fill_part != 1.0:
            inner_radius = outer_radius * (1-fill_part)
            path.addEllipse(center, inner_radius, inner_radius)
        self._painter.fillPath(path, color)

    def paint_pixmap(self, center: QPoint, pixmap: QPixmap):
        self._painter.drawPixmap(
            QPoint(
                center.x() - pixmap.width()//2,
                center.y() - pixmap.height()//2),
            pixmap
        )

    def end(self):
        self._painter.end()
