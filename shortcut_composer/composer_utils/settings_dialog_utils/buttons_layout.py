from typing import Callable
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QAbstractButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt


class ButtonsLayout(QVBoxLayout):

    def __init__(self, handle_buttons: Callable[[QAbstractButton], None]):
        super().__init__()

        buttons = (
            QDialogButtonBox.Ok |
            QDialogButtonBox.Apply |
            QDialogButtonBox.Reset |
            QDialogButtonBox.Cancel
        )
        self._button_box = QDialogButtonBox(buttons)  # type: ignore
        self._button_box.clicked.connect(handle_buttons)

        self.addWidget(self._button_box)
        self.setAlignment(Qt.AlignBottom)

    def get_button_role(self, button: QAbstractButton) \
            -> QDialogButtonBox.ButtonRole:
        return self._button_box.buttonRole(button)
