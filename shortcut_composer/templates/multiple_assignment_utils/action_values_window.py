# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

from config_system import Field
from composer_utils.layouts import ButtonsLayout
from .action_values import ActionValues


class ActionValuesWindow(QWidget):
    """Tab in which user can change values used in actions and their order."""

    def __init__(self, enum_type: Type[Enum], config: Field) -> None:
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.Tool)  # type: ignore
        layout = QVBoxLayout()

        self._config = config
        self.widget = ActionValues(enum_type, config)
        layout.addWidget(self.widget)

        layout.addLayout(ButtonsLayout(
            ok_callback=self.ok,
            apply_callback=self.apply,
            reset_callback=self.reset,
            cancel_callback=self.hide))

        self.setLayout(layout)

    def show(self) -> None:
        self.refresh()
        return super().show()

    def ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self.apply()
        self.hide()

    def reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        self._config.reset_default()
        self.refresh()

    def apply(self) -> None:
        self.widget.apply()

    def refresh(self) -> None:
        self.widget.refresh()
