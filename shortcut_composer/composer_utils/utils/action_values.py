# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Set

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QLabel,
)

from api_krita import Krita
from ..config import Config
from .value_list import ValueList


class ActionValues(QWidget):
    def __init__(self, allowed_values: Set[str], config: Config) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.allowed_values = set(allowed_values)
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

        layout.addLayout(self._labeled_list(self.available_list, "Available:"))
        layout.addLayout(control_layout)
        layout.addLayout(self._labeled_list(self.current_list, "Selected:"))

        self.setLayout(layout)

    def _labeled_list(self, value_list: ValueList, text: str) -> QVBoxLayout:
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(value_list)
        return layout

    def add(self):
        for item in self.available_list.selected:
            self.current_list.insert(
                position=self.current_list.current_row,
                value=item.text(),
            )
            self.available_list.remove(name=item.text(),)

    def remove(self):
        selected = [item.text() for item in self.current_list.selected]
        self.current_list.remove_selected()
        new_available = set(self.available_list.get_all()) | set(selected)
        self.available_list.clear()
        self.available_list.addItems(sorted(new_available))

    def apply(self):
        texts = []
        for row in range(self.current_list.count()):
            texts.append(self.current_list.item(row).text())
        self.config.write("\t".join(texts))

    def refresh(self):
        self.current_list.clear()
        current: str = self.config.read()
        current_list = current.split("\t")
        self.current_list.addItems(current_list)

        self.available_list.clear()
        allowed_items = sorted(self.allowed_values - set(current_list))
        self.available_list.addItems(allowed_items)
