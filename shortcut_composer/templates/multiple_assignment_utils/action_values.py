# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel)

from api_krita import Krita
from config_system import Field
from .value_list import ValueList


class ActionValues(QWidget):
    """
    Widget for selecting values and their order available as Enum.

    Consists of two lists next to each other. Values from the left
    represent all unused Enum values. They can be moved to the list of
    selected values on the right.

    Elements are moved between lists using two buttons. Widget supports
    moving multiple values at once. Drag&drop allows to change order in
    the list of selected values.
    """

    def __init__(self, enum_type: Type[Enum], config: Field[list[Enum]]):
        super().__init__()

        layout = QHBoxLayout()
        self.enum_type = enum_type
        self.config = config

        self.available_list = ValueList(movable=False, parent=self)
        self.current_list = ValueList(movable=True, parent=self)

        add_button = QPushButton(Krita.get_icon("list-add"), "")
        add_button.setStyleSheet("background-color : green")
        add_button.setFixedHeight(add_button.sizeHint().height()*3)
        add_button.clicked.connect(self.add)

        remove_button = QPushButton(Krita.get_icon("deletelayer"), "")
        remove_button.setStyleSheet("background-color : red")
        remove_button.setFixedHeight(remove_button.sizeHint().height()*3)
        remove_button.clicked.connect(self.remove)

        control_layout = QVBoxLayout()
        control_layout.addStretch()
        control_layout.addWidget(add_button)
        control_layout.addWidget(remove_button)
        control_layout.addStretch()

        layout.addLayout(self._add_label(self.available_list, "Available:"))
        layout.addLayout(control_layout)
        layout.addLayout(self._add_label(self.current_list, "Selected:"))

        self.setLayout(layout)

    def _add_label(self, value_list: ValueList, text: str) -> QVBoxLayout:
        """Adds a label on top of the list area."""
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(value_list)
        return layout

    def add(self) -> None:
        """Move mouse-selected values from the left list to the right."""
        for value in self.available_list.selected:
            self.current_list.insert(
                position=self.current_list.current_row,
                value=value)
            self.available_list.remove(value=value,)

    def remove(self) -> None:
        """Move mouse-selected values from the right list to the left."""
        selected = self.current_list.selected
        self.current_list.remove_selected()
        new_available = set(self.available_list.get_all()) | set(selected)
        self.available_list.clear()
        self.available_list.addItems(sorted(new_available))

    def apply(self) -> None:
        """Save the right list into kritarc."""
        to_write: list[Enum] = []
        for row in range(self.current_list.count()):
            text = self.current_list.item(row).text()
            to_write.append(self.enum_type[text])

        self.config.write(to_write)

    def refresh(self) -> None:
        """Refresh right list with kritarc values and left one accordingly."""
        self.current_list.clear()
        current_list = self.config.read()
        text_list = [item.name for item in current_list]
        self.current_list.addItems(text_list)

        self.available_list.clear()
        allowed_items = sorted(set(self._allowed_values) - set(text_list))
        self.available_list.addItems(allowed_items)

    @property
    def _allowed_values(self) -> list[str]:
        """Return list of all available values using the enum type."""
        return self.enum_type._member_names_
