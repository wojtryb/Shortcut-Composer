# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, NamedTuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QLabel,
    QGridLayout,
    QVBoxLayout)

from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_utils import create_label_widget
from ..pie_style import PieStyle


class ChildInstruction:
    """Logic of displaying widget text in passed QLabel."""

    def __init__(self, display_label: QLabel) -> None:
        self._display_label = display_label

    def on_enter(self, label: Label) -> None:
        """Set text of label which was entered with mouse."""
        self._display_label.setText(str(label.value))

    def on_leave(self, label: Label) -> None:
        """Reset text after mouse leaves the widget."""
        self._display_label.setText("")


class ScrollArea(QWidget):
    def __init__(
        self,
        values: List[Label],
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        super().__init__(parent)
        self._area = QScrollArea()
        self._area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self._area.setWidgetResizable(True)

        self._style = style
        self.labels = values

        self._scroll_area_layout = ScrollAreaLayout(columns, self)
        self._active_label_display = QLabel(self)
        self._children_list = self._create_children()

        layout = QVBoxLayout()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self._scroll_area_layout)
        self._area.setWidget(scroll_widget)
        layout.addWidget(self._area)
        layout.addWidget(self._active_label_display)
        self.setLayout(layout)

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
            child.add_instruction(ChildInstruction(self._active_label_display))
            children.append(child)
            self._scroll_area_layout.append(child)
        return children


class GridPosition(NamedTuple):
    gridrow: int
    gridcol: int


class ScrollAreaLayout(QGridLayout):
    def __init__(self, max_columns: int, owner: QWidget):
        super().__init__()
        self.widgets: List[QWidget] = []
        self._max_columns = max_columns
        self._items_in_group = 2*max_columns - 1
        self._owner = owner

    def __len__(self) -> int:
        return len(self.widgets)

    def _get_position(self, index: int) -> GridPosition:
        group, item = divmod(index, self._items_in_group)

        if item < self._max_columns:
            return GridPosition(gridrow=group*4, gridcol=item*2)

        col = item-self._max_columns
        return GridPosition(gridrow=group*4+2, gridcol=col*2+1)

    def _new_position(self) -> GridPosition:
        return self._get_position(len(self.widgets))

    def append(self, widget: QWidget) -> None:
        if widget in self.widgets:
            return
        widget.setParent(self._owner)
        widget.show()
        self.widgets.append(widget)
        self.addWidget(widget, *self._new_position(), 2, 2)
        self._refresh()

    def _refresh(self):
        for i, widget in enumerate(self.widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2)
