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
from ..krita_setting import write_setting


class ComboBoxes(QGridLayout):

    def __init__(self):
        QGridLayout.__init__(self)
        self.setAlignment(Qt.AlignTop)
        self.combo_boxes: Dict[Config, QComboBox] = {}
        self._row_counter = count()

        self._add_row(Config.TAG_RED)
        self._add_row(Config.TAG_GREEN)
        self._add_row(Config.TAG_BLUE)

    def _add_row(self, config: Config):
        row_id = next(self._row_counter)
        label = QLabel(config.value)
        label.setFixedWidth(100)
        self.addWidget(label, row_id, 0)
        self.addWidget(self._create_combobox(config), row_id, 1)

    def _create_combobox(self, config: Config):
        combo_box = QComboBox()
        combo_box.setObjectName(config.value)
        self.combo_boxes[config] = combo_box
        return combo_box

    def refresh(self):
        with Database() as database:
            tags = database.get_brush_tags()

        for config, combo_box in self.combo_boxes.items():
            combo_box.clear()
            combo_box.addItems(sorted(tags, key=str.lower))
            combo_box.setCurrentText(config.get())

    def apply(self):
        for combo in self.combo_boxes.values():
            write_setting(
                name=combo.objectName(),
                value=combo.currentText()
            )
