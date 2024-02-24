# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QListWidget, QWidget


class ValueList(QListWidget):
    """
    List widget with multi-selection and convenience methods.

    When movable, elements of list can be reordered with drag and drop.
    """

    def __init__(self, movable: bool, parent: QWidget | None = None):
        super().__init__(parent)
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        self.setMaximumWidth(200)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if movable:
            self.setDragDropMode(QAbstractItemView.InternalMove)

    @property
    def current_row(self) -> int:
        """Return selected row id, or the last id if none is selected."""
        if not self.selectedIndexes():
            return self.count()
        return self.currentRow()

    @property
    def selected(self) -> list[str]:
        """Return a list of all selected string values."""
        selected = self.selectedIndexes()
        indices = [item.row() for item in selected]
        items = [self.item(index) for index in indices]
        return [item.text() for item in items]

    def insert(self, position: int, value: str) -> None:
        """Add new string `value` after the item at given `position`."""
        self.insertItem(position+1, value)
        self.clearSelection()
        self.setCurrentRow(position+1)

    def get_all(self) -> list[str]:
        """Get list of all the strings in the list."""
        items: list[str] = []
        for i in range(self.count()):
            items.append(self.item(i).text())
        return items

    def remove(self, value: str) -> None:
        """Remove strings by passed value and select the previous one."""
        for item in self.findItems(value, Qt.MatchExactly):
            index = self.row(item)
            self.takeItem(index)
            self.setCurrentRow(index-1)

    def remove_selected(self) -> None:
        """Remove all the selected values."""
        for item in self.selected:
            self.remove(item)
