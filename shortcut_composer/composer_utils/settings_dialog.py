from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QVBoxLayout,
    QDialog,
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor

from api_krita import Krita
from .config import Config

from .settings_dialog_utils import Comboboxes, Forms


class SettingsDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Shortcut composer settings")

        self.comboboxes = Comboboxes()
        self.forms = Forms()
        ending_layout = self._create_ending_layout()

        layout = QVBoxLayout()
        layout.addLayout(self.comboboxes)
        layout.addLayout(self.forms)
        layout.addLayout(ending_layout)

        self.setLayout(layout)

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
            self._apply()
        elif role == QDialogButtonBox.ResetRole:
            Config.reset_defaults()
            self._refresh()
        elif role == QDialogButtonBox.AcceptRole:
            self._apply()
            self.hide()
        elif role == QDialogButtonBox.RejectRole:
            self.hide()

    def _apply(self):
        self.comboboxes.apply()
        self.forms.apply()
        Krita.trigger_action("Reload Shortcut Composer")

    def _refresh(self):
        self.comboboxes.refresh()
        self.forms.refresh()

    def show(self) -> None:
        self._refresh()
        self.move(QCursor.pos())
        return super().show()
