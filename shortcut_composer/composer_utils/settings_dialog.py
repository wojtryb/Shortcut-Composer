from typing import List
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QVBoxLayout,
    QGridLayout,
    QComboBox,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor
from api_krita.wrappers import Database
from api_krita import Krita


class SettingsDialog(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Shortcut composer settings")

        self.combo_boxes: List[QComboBox] = []

        button_layout = self._create_button_layout()
        combo_layout = self._create_combobox_layout()

        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _create_button_layout(self):
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        button_box = QDialogButtonBox(buttons)  # type: ignore
        button_box.accepted.connect(self._handle_ok_button)
        button_box.rejected.connect(self.hide)

        button_layout = QVBoxLayout()
        button_layout.addWidget(QLabel("Pressing ok reloads the plugin."))
        button_layout.addWidget(button_box)
        button_layout.setAlignment(Qt.AlignBottom)

        return button_layout

    def _handle_ok_button(self):
        for combo in self.combo_boxes:
            Krita.write_setting(
                group="ShortcutComposer",
                name=combo.objectName(),
                value=combo.currentText()
            )
            Krita.trigger_action("Reload Shortcut Composer")
        self.hide()

    def _create_combobox_layout(self):
        combo_layout = QGridLayout()
        combo_layout.setAlignment(Qt.AlignTop)

        def add_row(name: str, row_id: int):
            label = QLabel(name)
            label.setFixedWidth(100)
            combo_layout.addWidget(label, row_id, 0)
            combo_box = self._create_combobox(name)
            combo_layout.addWidget(combo_box, row_id, 1)

        add_row("Tag (green)", 0)
        add_row("Tag (blue)", 1)
        add_row("Tag (red)", 2)

        return combo_layout

    def _create_combobox(self, name: str):
        combo_box = QComboBox(self)
        combo_box.setObjectName(name)
        self.combo_boxes.append(combo_box)
        return combo_box

    def show(self) -> None:
        self._refresh_comboboxes()
        self.move(QCursor.pos())
        return super().show()

    def _refresh_comboboxes(self):
        with Database() as database:
            tags = database.get_brush_tags()

        for combo_box in self.combo_boxes:
            combo_box.clear()
            combo_box.addItems(sorted(tags))
            combo_box.setCurrentText(Krita.read_setting(
                group="ShortcutComposer",
                name=combo_box.objectName(),
                default="RGBA",
            ))
