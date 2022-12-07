from typing import TypeVar, List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor

from shortcut_composer_config import PIE_DEADZONE_PX
from api_krita.pyqt import Painter
from .pie_style import PieStyle
from .label_holder import LabelHolder
from .label_painter import pick_correct_painter, LabelPainter

T = TypeVar('T')


class PieWidget(QWidget):
    def __init__(
        self,
        labels: LabelHolder,
        style: PieStyle,
        parent=None
    ):
        QWidget.__init__(self, parent)
        self._style = style
        self._labels = labels
        self._label_painters = self._create_label_painters()

        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window |  # type: ignore
            Qt.FramelessWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Pie Menu")
        size = (self._style.widget_radius)*2
        self.setGeometry(0, 0, size, size)

    @property
    def center(self) -> QPoint:
        return QPoint(self._style.widget_radius, self._style.widget_radius)

    @property
    def center_global(self) -> QPoint:
        return self.pos() + self.center  # type: ignore

    @property
    def outer_radius(self) -> int:
        return self._style.pie_radius - self._style.border_thickness//2

    def move_center(self, x: int, y: int) -> None:
        self.move(x-self._style.widget_radius, y-self._style.widget_radius)

    def paintEvent(self, event) -> None:
        with Painter(self, event) as painter:
            self._paint_base_wheel(painter)
            self._paint_active_pie(painter)
            self._paint_base_border(painter)
            self._paint_deadzone_indicator(painter)

            for label_painter in self._label_painters:
                label_painter.paint(painter)

    def _paint_base_wheel(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=self.outer_radius,
            color=self._style.area_color,
            thickness=self._style.area_thickness,
        )

    def _paint_base_border(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._style.pie_radius - self._style.area_thickness,
            color=self._style.border_color,
            thickness=self._style.border_thickness,
        )

    def _paint_deadzone_indicator(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=PIE_DEADZONE_PX,
            color=QColor(255, 255, 255, 255),
            thickness=1,
        )

    def _paint_active_pie(self, painter: Painter):
        if not self._labels.active:
            return

        painter.paint_pie(
            center=self.center,
            outer_radius=self.outer_radius,
            angle=self._labels.active.angle,
            span=360//len(self._label_painters),
            color=self._style.active_color,
            thickness=self._style.area_thickness,
        )

    def _create_label_painters(self) -> List[LabelPainter]:
        painters = []
        for label in self._labels:
            painters.append(pick_correct_painter(
                widget=self,
                style=self._style,
                label=label,
            ))
        return painters
