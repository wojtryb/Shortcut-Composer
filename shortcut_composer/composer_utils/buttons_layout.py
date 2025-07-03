# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable
from dataclasses import dataclass

from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from api_krita.pyqt import SafeConfirmButton

EmptyCallback = Callable[[], None]


@dataclass
class ButtonsLayout(QHBoxLayout):
    """Dialog zone consisting of buttons for applying/rejecting the changes."""

    def __init__(
        self,
        reset_callback: EmptyCallback = lambda: None,
        cancel_callback: EmptyCallback = lambda: None,
        apply_callback: EmptyCallback = lambda: None,
        ok_callback: EmptyCallback = lambda: None,
    ) -> None:
        super().__init__()

        reset_button = SafeConfirmButton(text="Reset")
        reset_button.setFixedSize(reset_button.sizeHint())
        reset_button.clicked.connect(reset_callback)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(cancel_callback)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(apply_callback)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(ok_callback)

        self.addWidget(reset_button)
        self.addStretch()
        self.addWidget(cancel_button)
        self.addWidget(apply_button)
        self.addWidget(ok_button)
