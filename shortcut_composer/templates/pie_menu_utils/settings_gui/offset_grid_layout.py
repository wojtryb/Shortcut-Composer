# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, NamedTuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout

from ..label_widget import LabelWidget


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
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # type: ignore
        self.setVerticalSpacing(5)
        self.setHorizontalSpacing(5)

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
                kept_widget.hide()
                self.removeWidget(kept_widget)
                kept_widget.setParent(None)  # type: ignore

        self._widgets.clear()
        self.extend(widgets)
        self._refresh()

    def _refresh(self):
        """Refresh the layout by adding all the internal widgets to it."""
        for i, widget in enumerate(self._widgets):
            self.addWidget(widget, *self._get_position(i), 2, 2)
