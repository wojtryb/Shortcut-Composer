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


class ScrollAreaLayout(QGridLayout):
    def __init__(self, cols: int):
        super().__init__()
        self.widgets: List[QWidget] = []
        self._max_rows = cols
        self._uniques = 2*cols - 1

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
        self.widgets.append(widget)
        self.addWidget(widget, *self._new_position(), 2, 2)
        self._refresh()

    def pop(self, index: int):
        self.widgets.pop(index)
        self._refresh()

    def insert(self, index: int, widget: QWidget):
        self.widgets.insert(index, widget)
        self._refresh()

    def _refresh(self):
        for i, widget in enumerate(self.widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2)


class ScrollArea(AnimatedWidget, BaseWidget):
    def __init__(
        self,
        cols: int,
        unused_values: List[Label],
        style: PieStyle,
        parent=None
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setGeometry(0, 0, style.widget_radius*2, style.widget_radius*2)

        self._style = style
        self._layout = ScrollAreaLayout(cols)

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint))
        self.setCursor(Qt.ArrowCursor)

        scroll_internal = QWidget()
        self.labels = unused_values
        self.children_list = self._create_children()

        for child in self.children_list:
            child.setFixedSize(self._style.icon_radius*2, self._style.icon_radius*2)
            self._layout.append(child)

        scroll_internal.setLayout(self._layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_internal)
        scroll_area.setFixedWidth(scroll_internal.width() + self._style.icon_radius)
        scroll_area.setWidgetResizable(True)

        main_layout = QHBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(scroll_area)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self.hide()

    def _create_children(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        children: List[LabelWidget] = []
        for label in self.labels:
            children.append(create_label_widget(label, self._style, self))
        return children

    def move_to_pie_side(self):
        self.move_center(QCursor().pos() + QPoint(self.width(), 0))  # type: ignore
