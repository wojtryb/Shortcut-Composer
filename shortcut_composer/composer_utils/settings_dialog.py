from typing import List, Dict, Union
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QWidget,
    QLabel,
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor

from api_krita.wrappers import Database
from api_krita import Krita
from .config import Config
from .krita_setting import read_setting, write_setting


class SettingsDialog(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Shortcut composer settings")

        self.combo_boxes: List[QComboBox] = []
        self.forms: Dict[Config, Union[QSpinBox, QDoubleSpinBox]] = {}

        combo_layout = self._create_combobox_layout()
        form_layout = self._create_form_layout()
        ending_layout = self._create_ending_layout()

        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        layout.addLayout(form_layout)
        layout.addLayout(ending_layout)

        self.setLayout(layout)

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

    def _create_form_layout(self):
        form_layout = QFormLayout()

        def add_row(config: Config, is_int: bool):
            form = self._create_form(config, is_int)
            form_layout.addRow(config.value, form)

        add_row(Config.SHORT_VS_LONG_PRESS_TIME, is_int=False)
        add_row(Config.SLIDER_SENSITIVITY_SCALE, is_int=False)
        add_row(Config.SLIDER_DEADZONE, is_int=True)
        add_row(Config.FPS_LIMIT, is_int=True)
        add_row(Config.PIE_GLOBAL_SCALE, is_int=False)
        add_row(Config.PIE_ICON_GLOBAL_SCALE, is_int=False)
        add_row(Config.PIE_DEADZONE_GLOBAL_SCALE, is_int=False)

        self._refresh_forms()
        return form_layout

    def _refresh_forms(self):
        for config, form in self.forms.items():
            form.setValue(float(config.get()))  # type: ignore

    def _create_form(self, config: Config, is_int: bool):
        form = QSpinBox() if is_int else QDoubleSpinBox()
        form.setObjectName(config.value)
        form.setMinimum(0)
        form.setSingleStep(1 if is_int else 0.1)  # type: ignore

        self.forms[config] = form
        return form

    def _create_ending_layout(self):
        buttons = (
            QDialogButtonBox.Ok |
            QDialogButtonBox.Apply |
            QDialogButtonBox.Reset |
            QDialogButtonBox.Cancel
        )

        self.button_box = QDialogButtonBox(buttons)  # type: ignore
        self.button_box.clicked.connect(self._handle_click)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.button_box)
        button_layout.setAlignment(Qt.AlignBottom)

        return button_layout

    def _handle_click(self, button):
        role = self.button_box.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            self._apply_button()
        elif role == QDialogButtonBox.ResetRole:
            Config.reset_defaults()
            self._refresh_forms()
        elif role == QDialogButtonBox.AcceptRole:
            self._apply_button()
            self.hide()
        elif role == QDialogButtonBox.RejectRole:
            self.hide()

    def _apply_button(self):
        for combo in self.combo_boxes:
            write_setting(
                name=combo.objectName(),
                value=combo.currentText()
            )
        for form in self.forms.values():
            write_setting(
                name=form.objectName(),
                value=form.value()
            )
        Krita.trigger_action("Reload Shortcut Composer")

    def show(self) -> None:
        self._refresh_comboboxes()
        self._refresh_forms()
        self.move(QCursor.pos())
        return super().show()

    def _refresh_comboboxes(self):
        with Database() as database:
            tags = database.get_brush_tags()

        for combo_box in self.combo_boxes:
            combo_box.clear()
            combo_box.addItems(sorted(tags, key=str.lower))
            combo_box.setCurrentText(read_setting(
                name=combo_box.objectName(),
                default="RGBA",
            ))
