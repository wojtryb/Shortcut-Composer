# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Set

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QWidget,
)

from api_krita import Krita
from ..config import Config
from .value_list import ValueList


class PieValues(QWidget):
    def __init__(self, allowed_values: Set[str], config: Config) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.allowed_values = sorted(allowed_values)
        self.config = config

        self.list_widget = ValueList(self)

        self.combo_box = QComboBox()
        self.combo_box.addItems(self.allowed_values)

        add_button = QPushButton(Krita.get_icon("list-add"), "")
        add_button.setFixedWidth(40)
        add_button.clicked.connect(self.add)

        remove_button = QPushButton(Krita.get_icon("deletelayer"), "")
        remove_button.setFixedWidth(40)
        remove_button.clicked.connect(self.list_widget.remove_selected)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.combo_box)
        control_layout.addWidget(add_button)
        control_layout.addWidget(remove_button)

        layout.addLayout(control_layout)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def add(self):
        self.list_widget.insert(
            position=self.list_widget.current_row,
            value=self.combo_box.currentText()
        )

    def apply(self):
        texts = []
        for row in range(self.list_widget.count()):
            texts.append(self.list_widget.item(row).text())
        self.config.write(";".join(texts))

    def refresh(self):
        self.list_widget.clear()
        currently_set: str = self.config.read()
        self.list_widget.addItems(currently_set.split(";"))
