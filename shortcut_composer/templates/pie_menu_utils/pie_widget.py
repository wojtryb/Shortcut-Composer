from typing import TypeVar
import math

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (
    QColor,
)

from core_components import Controller
from api_krita.pyqt import Painter, pick_correct_label
from .label_holder import LabelHolder

T = TypeVar('T')


class PieWidget(QWidget):
    def __init__(
        self,
        controller: Controller,
        values: list,
        pie_radius_px: int,
        icon_radius_px: int,
        color: QColor,
        parent=None
    ):
        QWidget.__init__(self, parent)
        self._controller = controller
        self._values = values
        self._pie_radius_px = pie_radius_px
        self._icon_radius_px = icon_radius_px
        self._widget_radius_px = pie_radius_px + icon_radius_px
        self._border_thickness = self._icon_radius_px*0.1
        self._area_thickness = self._pie_radius_px*0.4
        self._color = color
        self._border_color = QColor(55, 55, 55, 255)

        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window |  # type: ignore
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Pie Menu")
        size = (self._widget_radius_px)*2
        self.setGeometry(0, 0, size, size)

        self.labels = self._create_labels()
        self.changed = False

    @property
    def center(self) -> QPoint:
        return QPoint(self._widget_radius_px, self._widget_radius_px)

    def move_center(self, x: int, y: int) -> None:
        self.move(x-self._widget_radius_px, y-self._widget_radius_px)

    def show(self) -> None:
        super().show()
        self.changed = True

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if not self.changed:
            return

        painter = Painter(self, event)
        self._paint_wheel(painter)

        for label in self.labels:
            label.paint(painter)

        painter.end()
        self.changed = False

    def _paint_wheel(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._pie_radius_px-self._border_thickness//2,
            color=self._color,
            thickness=self._area_thickness,
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._pie_radius_px,
            thickness=self._border_thickness,
            color=self._border_color,
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._pie_radius_px - self._area_thickness,
            color=self._border_color,
            thickness=self._border_thickness,
        )

    # wyzej, do pluginu
    def _center_from_angle(self, angle: int, distance: int) -> QPoint:
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._widget_radius_px + distance*math.sin(rad_angle)),
            round(self._widget_radius_px - distance*math.cos(rad_angle)),
        )

    # wyzej, do pluginu
    def _create_labels(self) -> LabelHolder:
        labels = LabelHolder()

        iterator = range(0, 360, round(360/len(self._values)))
        for value, angle in zip(self._values, iterator):
            distance = self._pie_radius_px
            label_center = self._center_from_angle(angle, distance)

            labels[angle] = pick_correct_label(
                widget=self,
                center=label_center,
                radius=self._icon_radius_px,
                value=value,
                display_value=self._controller.get_label(value),
                bg_color=self._border_color
            )
        return labels
