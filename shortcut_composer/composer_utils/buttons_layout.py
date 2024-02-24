# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable
from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialogButtonBox, QAbstractButton, QVBoxLayout

EmptyCallback = Callable[[], None]


@dataclass
class ButtonsLayout(QVBoxLayout):
    """Dialog zone consisting of buttons for applying/rejecting the changes."""

    ok_callback: EmptyCallback = lambda: None
    apply_callback: EmptyCallback = lambda: None
    reset_callback: EmptyCallback = lambda: None
    cancel_callback: EmptyCallback = lambda: None

    def __post_init__(self) -> None:
        super().__init__()

        self._button_box = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Apply |
            QDialogButtonBox.Reset |
            QDialogButtonBox.Cancel  # type: ignore
        )
        self._button_box.clicked.connect(self._handle_buttons)

        self.addWidget(self._button_box)
        self.setAlignment(Qt.AlignBottom)

    def _handle_buttons(self, button: QAbstractButton) -> None:
        """React to one of the buttons being pressed."""
        role = self._button_box.buttonRole(button)
        if role == QDialogButtonBox.AcceptRole:
            self.ok_callback()
        elif role == QDialogButtonBox.ApplyRole:
            self.apply_callback()
        elif role == QDialogButtonBox.ResetRole:
            self.reset_callback()
        elif role == QDialogButtonBox.RejectRole:
            self.cancel_callback()
