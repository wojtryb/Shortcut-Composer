# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QDialog
from PyQt5.QtCore import Qt

from config_system import Field
from composer_utils import ButtonsLayout
from .action_values import ActionValues


class ActionValuesWindow(QDialog):
    """Tab in which user can change action enums and their order."""

    def __init__(self, enum_type: Type[Enum], config: Field[list[Enum]]):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)  # type: ignore
        layout = QVBoxLayout()

        self._config = config
        self.widget = ActionValues(enum_type, config)
        layout.addWidget(self.widget)

        layout.addLayout(ButtonsLayout(
            ok_callback=self._ok,
            apply_callback=self._apply,
            reset_callback=self._reset,
            cancel_callback=self.hide))

        self.setLayout(layout)

    def show(self) -> None:
        """Refresh the widget before showing it."""
        self._refresh()
        return super().show()

    def _ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self._apply()
        self.hide()

    def _reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        self._config.reset_default()
        self._refresh()

    def _apply(self) -> None:
        """Apply changes in held widget."""
        self.widget.apply()

    def _refresh(self) -> None:
        """Refresh the held widget."""
        self.widget.refresh()
