from typing import List
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QLabel,
    QGridLayout,
    QHBoxLayout,
)
from api_krita.pyqt import AnimatedWidget, BaseWidget
from composer_utils import Config


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
    def __init__(self, cols: int, parent=None):
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint))
        self.setCursor(Qt.CrossCursor)

        self.setGeometry(0, 0, 400, 300)
        self._layout = ScrollAreaLayout(cols)
        self.icon_size = 64

        scroll_internal = QWidget()
        for i in range(22):
            self.add_label(str(i))

        blue_label = QLabel("asd")
        blue_label.setFixedSize(QSize(self.icon_size, self.icon_size))
        blue_label.setStyleSheet("background-color : blue")
        self._layout.insert(10, blue_label)

        self._layout.pop(0)
        self._layout.pop(0)
        self._layout.pop(0)

        for i in range(5):
            self.add_label(str(i))

        scroll_internal.setLayout(self._layout)

        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_internal)
        scroll_area.setFixedWidth(scroll_internal.width() + self.icon_size//2)
        scroll_area.setWidgetResizable(True)

        main_layout = QHBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(scroll_area)
        main_layout.addStretch()
        self.setLayout(main_layout)

        self.hide()

    def add_label(self, name: str):
        label = QLabel(str(name))
        label.setFixedSize(QSize(self.icon_size, self.icon_size))
        label.setStyleSheet("background-color : green")
        self._layout.append(label)
