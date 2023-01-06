from typing import List
from PyQt5.QtWidgets import (
    QGridLayout,
    QComboBox,
    QLabel,
)
from PyQt5.QtCore import Qt

from api_krita.wrappers import Database
from ..krita_setting import read_setting, write_setting


class Comboboxes(QGridLayout):

    def __init__(self):
        QGridLayout.__init__(self)
        self.setAlignment(Qt.AlignTop)
        self.combo_boxes: List[QComboBox] = []

        def add_row(name: str, row_id: int):
            label = QLabel(name)
            label.setFixedWidth(100)
            self.addWidget(label, row_id, 0)
            combo_box = self._create_combobox(name)
            self.addWidget(combo_box, row_id, 1)

        add_row("Tag (green)", 0)
        add_row("Tag (blue)", 1)
        add_row("Tag (red)", 2)

    def refresh(self):
        with Database() as database:
            tags = database.get_brush_tags()

        for combo_box in self.combo_boxes:
            combo_box.clear()
            combo_box.addItems(sorted(tags, key=str.lower))
            combo_box.setCurrentText(read_setting(
                name=combo_box.objectName(),
                default="RGBA",
            ))

    def apply(self):
        for combo in self.combo_boxes:
            write_setting(
                name=combo.objectName(),
                value=combo.currentText()
            )

    def _create_combobox(self, name: str):
        combo_box = QComboBox()
        combo_box.setObjectName(name)
        self.combo_boxes.append(combo_box)
        return combo_box
