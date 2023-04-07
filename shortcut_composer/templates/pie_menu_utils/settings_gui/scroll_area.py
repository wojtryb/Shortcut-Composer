from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QGridLayout)

from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_utils import create_label_widget
from ..pie_style import PieStyle


class ScrollArea(QScrollArea):
    def __init__(
        self,
        values: List[Label],
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        super().__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        self._style = style
        self.labels = values

        self._scroll_area_layout = ScrollAreaLayout(columns, self)
        self._children_list = self._create_children()

        scroll_widget = QWidget()
        scroll_widget.setLayout(self._scroll_area_layout)
        self.setWidget(scroll_widget)

    def _create_children(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        children: List[LabelWidget] = []

        for label in self.labels:
            child = create_label_widget(
                label=label,
                style=self._style,
                parent=self,
                is_unscaled=True)
            child.setFixedSize(child.icon_radius*2, child.icon_radius*2)
            child.draggable = True
            children.append(child)
            self._scroll_area_layout.append(children[-1])
        return children


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
        widget = self.widgets.pop(index)
        self.removeWidget(widget)
        self._refresh()
        return widget

    def remove(self, widget: QWidget):
        for index, held_widget in enumerate(self.widgets):
            if held_widget == widget:
                return self.pop(index)

    def insert(self, index: int, widget: QWidget):
        self.widgets.insert(index, widget)
        self._refresh()

    def _refresh(self):
        for i, widget in enumerate(self.widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2)
