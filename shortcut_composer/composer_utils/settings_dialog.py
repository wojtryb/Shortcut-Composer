from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QAbstractButton,
    QVBoxLayout,
    QDialog,
)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCursor

from api_krita import Krita
from .config import Config
from .settings_dialog_utils import ComboBoxesLayout, FormsLayout, ButtonsLayout


class SettingsDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Shortcut composer settings")

        self._combo_boxes_layout = ComboBoxesLayout()
        self._forms_layout = FormsLayout()
        self._buttons_layout = ButtonsLayout(self._handle_any_button_click)

        full_layout = QVBoxLayout()
        full_layout.addLayout(self._combo_boxes_layout)
        full_layout.addLayout(self._forms_layout)
        full_layout.addLayout(self._buttons_layout)
        self.setLayout(full_layout)

    def _handle_any_button_click(self, button: QAbstractButton):
        role = self._buttons_layout.get_button_role(button)
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
        self._combo_boxes_layout.apply()
        self._forms_layout.apply()
        Krita.trigger_action("Reload Shortcut Composer")

    def _refresh(self):
        self._combo_boxes_layout.refresh()
        self._forms_layout.refresh()

    def show(self) -> None:
        self._refresh()
        self.move(QCursor.pos())
        return super().show()
