# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QListWidget,
    QWidget,
)


class ValueList(QListWidget):
    def __init__(self, movable: bool, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        self.setMaximumWidth(200)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if movable:
            self.setDragDropMode(QAbstractItemView.InternalMove)

    @property
    def current_row(self):
        if not self.selectedIndexes():
            return self.count()
        return self.currentRow()

    def insert(self, position: int, value: str):
        self.insertItem(position+1, value)
        self.clearSelection()
        self.setCurrentRow(position+1)

    def get_all(self):
        items: List[str] = []
        for i in range(self.count()):
            items.append(self.item(i).text())
        return items

    @property
    def selected(self):
        selected = self.selectedIndexes()
        return [self.item(item.row()) for item in selected]

    def remove(self, name: str):
        for item in self.findItems(name, Qt.MatchExactly):
            self.takeItem(self.row(item))

    def remove_selected(self):
        selected = self.selectedIndexes()
        indices = [item.row() for item in selected]
        for index in sorted(indices, reverse=True):
            self.takeItem(index)

        if selected:
            first_deleted_row = min([item.row() for item in selected])
            self.clearSelection()
            self.setCurrentRow(first_deleted_row-1)
