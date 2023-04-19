# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from typing import List, NamedTuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout)

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
        self._display_label.setText(str(label.pretty_name))

    def on_leave(self, label: Label) -> None:
        """Reset text after mouse leaves the widget."""
        self._display_label.setText("")


class ScrollArea(QWidget):
    """
    Widget containing a scrollable list of PieWidgets.

    Widgets are created based on the passed labels and then made
    publically available in `children_list` attribute, so that the owner
    of the class can change their state (draggable, enabled).

    ScrollArea comes with embedded QLabel showing the name of the
    children widget over which mouse was hovered.
    """

    def __init__(
        self,
        labels: List[Label],
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        super().__init__(parent)
        self._style = style
        self._labels = labels

        scroll_widget = QWidget()
        self._scroll_area_layout = OffsetGridLayout(columns, self)
        scroll_widget.setLayout(self._scroll_area_layout)

        area = QScrollArea()
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        area.setWidgetResizable(True)
        area.setWidget(scroll_widget)

        footer = QHBoxLayout()
        self._active_label_display = QLabel(self)
        footer.addWidget(self._active_label_display, 1)
        self._search_bar = QLineEdit(self)
        self._search_bar.setPlaceholderText("Search")
        self._search_bar.setClearButtonEnabled(True)
        footer.addWidget(self._search_bar, 1)
        self._search_bar.textChanged.connect(self._apply_search_bar_filter)

        layout = QVBoxLayout()
        layout.addWidget(area)
        layout.addLayout(footer)
        self.setLayout(layout)

        self.children_list = self._create_children()

    def _create_children(self) -> List[LabelWidget]:
        """Create LabelWidgets that represent the labels."""
        children: List[LabelWidget] = []

        for label in self._labels:
            child = create_label_widget(
                label=label,
                style=self._style,
                parent=self,
                is_unscaled=True)
            child.setFixedSize(child.icon_radius*2, child.icon_radius*2)
            child.draggable = True
            child.add_instruction(ChildInstruction(self._active_label_display))
            children.append(child)

        self._scroll_area_layout.extend(children)
        return children

    def _apply_search_bar_filter(self):
        """Replace widgets in layout with those thich match the filter."""
        pattern = self._search_bar.text()
        regex = re.compile(pattern, flags=re.IGNORECASE)

        children = [child for child in self.children_list
                    if regex.search(child.label.pretty_name)]

        self._scroll_area_layout.replace(children)


class GridPosition(NamedTuple):
    gridrow: int
    gridcol: int


class OffsetGridLayout(QGridLayout):
    """
    Layout displaying widgets, as the grid in which even rows have offset.

    Even rows have one item less than uneven rows, and are moved half
    the widget width to make them overlap with each other.

    The layout acts like list of widgets it's responsibility is to
    automatically refresh, when changes are being made to it.

    Implemented using QGridLayout in which every widget uses 2x2 fields.

    max_columns -- Amount of widgets in uneven rows.
                   When set to 4, rows will cycle: (4, 3, 4, 3, 4...)
    group       -- Two consecutive rows of widgets.
                   When max_columns is 4 will consist of 7 (4+3) widgets
    """

    def __init__(self, max_columns: int, owner: QWidget):
        super().__init__()
        self._widgets: List[LabelWidget] = []
        self._max_columns = max_columns
        self._items_in_group = 2*max_columns - 1
        self._owner = owner

    def __len__(self) -> int:
        """Amount of held LabelWidgets."""
        return len(self._widgets)

    def _get_position(self, index: int) -> GridPosition:
        """Return a GridPosition (row, col) of it's widget."""
        group, item = divmod(index, self._items_in_group)

        if item < self._max_columns:
            return GridPosition(gridrow=group*4, gridcol=item*2)

        col = item-self._max_columns
        return GridPosition(gridrow=group*4+2, gridcol=col*2+1)

    def _internal_insert(self, index: int, widget: LabelWidget) -> None:
        """Insert widget at given index if not stored already."""
        if widget in self._widgets:
            return
        widget.setParent(self._owner)
        widget.show()
        self._widgets.insert(index, widget)

    def insert(self, index: int, widget: LabelWidget) -> None:
        """Insert the widget at given index and refresh the layout."""
        self._internal_insert(index, widget)
        self._refresh()

    def append(self, widget: LabelWidget) -> None:
        """Append the widget at the end and refresh the layout."""
        self._internal_insert(len(self), widget)
        self._refresh()

    def extend(self, widgets: List[LabelWidget]) -> None:
        """Extend layout with the given widgets and refresh the layout."""
        for widget in widgets:
            self._internal_insert(len(self), widget)
        self._refresh()

    def replace(self, widgets: List[LabelWidget]):
        """Replace all existing widgets with the ones provided."""
        if widgets == self._widgets:
            return

        for kept_widget in self._widgets:
            if kept_widget not in widgets:
                self.removeWidget(kept_widget)
                kept_widget.setParent(None)  # type: ignore

        self._widgets.clear()
        self.extend(widgets)
        self._refresh()

    def _refresh(self):
        """Refresh the layout by adding all the internal widgets to it."""
        align: Qt.AlignmentFlag = Qt.AlignTop | Qt.AlignLeft  # type: ignore
        for i, widget in enumerate(self._widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2, align)
