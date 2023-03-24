from typing import List
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QGridLayout,
    QHBoxLayout,
)
from api_krita.pyqt import AnimatedWidget, BaseWidget
from composer_utils import Config
from .label import Label
from .label_widget import LabelWidget
from .label_widget_utils import create_label_widget
from .pie_style import PieStyle


class PieSettings(AnimatedWidget, BaseWidget):
    def __init__(
        self,
        values: List[Label],
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setFixedHeight(style.widget_radius*2)

        self._style = style
        self.labels = values
        self.children_list = self._create_children()

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint))
        self.setCursor(Qt.ArrowCursor)

        self._scroll_area_layout = ScrollAreaLayout(columns, self)
        radius = self._style.icon_radius*2
        for child in self.children_list:
            child.setFixedSize(radius, radius)
            self._scroll_area_layout.append(child)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self._scroll_area_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFixedWidth(self._style.icon_radius*(columns*2+1))
        scroll_area.setWidgetResizable(True)

        pop_up_layout = QHBoxLayout(self)
        pop_up_layout.addStretch()
        pop_up_layout.addWidget(scroll_area)
        pop_up_layout.addStretch()
        self.setLayout(pop_up_layout)

        self.hide()

    def _create_children(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        children: List[LabelWidget] = []
        for label in self.labels:
            children.append(create_label_widget(label, self._style, self))
        return children

    def move_to_pie_side(self):
        offset = self.width()//2 + self._style.widget_radius * 1.05
        point = QPoint(round(offset),0)
        self.move_center(QCursor().pos() + point)  # type: ignore


class ScrollAreaLayout(QGridLayout):
    def __init__(self, cols: int, owner: QWidget):
        super().__init__()
        self.widgets: List[QWidget] = []
        self._max_rows = cols
        self._uniques = 2*cols - 1
        self._owner = owner

    def __len__(self):
        return len(self.widgets)

    def _get_position(self, index: int):
        row, col = divmod(index, self._uniques)
        if col < self._max_rows:
            return (row*4, col*2)
        return (row*4+2, (col-self._max_rows)*2+1)

    def _new_position(self):
        return self._get_position(len(self.widgets))

    def append(self, widget: QWidget):
        if widget in self.widgets:
            return
        widget.setParent(self._owner)
        widget.show()
        self.widgets.append(widget)
        self.addWidget(widget, *self._new_position(), 2, 2)
        self._refresh()

    def pop(self, index: int):
        self.widgets.pop(index)
        self._refresh()

    def remove(self, widget: QWidget):
        for index, held_widget in enumerate(self.widgets):
            if held_widget == widget:
                self.pop(index)
                return self._refresh()

    def insert(self, index: int, widget: QWidget):
        self.widgets.insert(index, widget)
        self._refresh()

    def _refresh(self):
        for i, widget in enumerate(self.widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2)
