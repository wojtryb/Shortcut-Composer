# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QListWidget,
    QWidget,
)


class ValueList(QListWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    @property
    def current_row(self):
        if not self.selectedIndexes():
            return self.count()
        return self.currentRow()

    def insert(self, position: int, value: str):
        self.insertItem(position+1, value)
        self.clearSelection()
        self.setCurrentRow(position+1)

    def remove_selected(self):
        selected = self.selectedIndexes()
        indices = [item.row() for item in selected]
        for index in sorted(indices, reverse=True):
            self.takeItem(index)

        if selected:
            first_deleted_row = min([item.row() for item in selected])
            self.clearSelection()
            self.setCurrentRow(first_deleted_row-1)
