from typing import TypeVar, List

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget

from core_components import Controller
from api_krita.pyqt import Painter
from .pie_style import PieStyle
from .label_holder import LabelHolder
from .label_painter import pick_correct_painter, LabelPainter

T = TypeVar('T')


class PieWidget(QWidget):
    def __init__(
        self,
        controller: Controller,
        labels: LabelHolder,
        style: PieStyle,
        parent=None
    ):
        QWidget.__init__(self, parent)
        self._controller = controller
        self._style = style
        self._label_painters = self._create_label_painters(labels)

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

        self.changed = False

    @property
    def center(self) -> QPoint:
        return QPoint(
            self._style.widget_radius,
            self._style.widget_radius)

    def move_center(self, x: int, y: int) -> None:
        self.move(
            x-self._style.widget_radius,
            y-self._style.widget_radius)

    def show(self) -> None:
        super().show()
        self.changed = True

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        if not self.changed:
            return

        painter = Painter(self, event)
        self._paint_wheel(painter)

        for label in self._label_painters:
            label.paint(painter)

        painter.end()
        self.changed = False

    def _paint_wheel(self, painter: Painter):
        painter.paint_wheel(
            center=self.center,
            outer_radius=(
                self._style.pie_radius
                - self._style.border_thickness//2),
            color=self._style.color,
            thickness=self._style.area_thickness,
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=self._style.pie_radius,
            thickness=self._style.border_thickness,
            color=self._style.border_color,
        )
        painter.paint_wheel(
            center=self.center,
            outer_radius=(
                self._style.pie_radius
                - self._style.area_thickness),
            color=self._style.border_color,
            thickness=self._style.border_thickness,
        )

    def _create_label_painters(self, labels: LabelHolder)\
            -> List[LabelPainter]:
        painters = []
        for label in labels:
            painters.append(pick_correct_painter(self, self._style, label))
        return painters
