# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict
from itertools import count
from PyQt5.QtWidgets import (
    QGridLayout,
    QComboBox,
    QLabel,
)
from PyQt5.QtCore import Qt

from api_krita.wrappers import Database
from ..config import Config


class ComboBoxesLayout(QGridLayout):
    """Dialog zone consisting of combo boxes."""

    def __init__(self) -> None:
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        self._combo_boxes: Dict[Config, QComboBox] = {}
        self._row_counter = count()

        self._add_label("Preset pie-menus mapping")
        self._add_row(Config.TAG_RED)
        self._add_row(Config.TAG_GREEN)
        self._add_row(Config.TAG_BLUE)

    def _add_row(self, config: Config) -> None:
        """Add a combobox to the layout along with its description."""
        row_id = next(self._row_counter)
        label = QLabel(config.value)
        label.setFixedWidth(100)
        self.addWidget(label, row_id, 0)
        self.addWidget(self._create_combobox(config), row_id, 1)

    def _add_label(self, text: str):
        row_id = next(self._row_counter)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addWidget(label, row_id, 0, 1, 2)

    def _create_combobox(self, config: Config) -> QComboBox:
        """Store and return combobox that represents given config field."""
        combo_box = QComboBox()
        combo_box.setObjectName(config.value)
        self._combo_boxes[config] = combo_box
        return combo_box

    def refresh(self) -> None:
        """Read list of tags and set it to all stored comboboxes."""
        with Database() as database:
            tags = database.get_brush_tags()

        for config, combo_box in self._combo_boxes.items():
            combo_box.clear()
            combo_box.addItems(sorted(tags, key=str.lower))
            combo_box.setCurrentText(config.read())

    def apply(self) -> None:
        """Write values from all stored comboboxes to krita config file."""
        for config, combo in self._combo_boxes.items():
            config.write(combo.currentText())
