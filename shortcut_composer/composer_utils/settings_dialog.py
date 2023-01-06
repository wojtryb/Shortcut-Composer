# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCursor

from api_krita import Krita
from .config import Config
from .settings_dialog_utils import (
    ComboBoxesLayout,
    SpinBoxesLayout,
    ButtonsLayout
)


class SettingsDialog(QDialog):
    """Dialog which allows to change global settings of the plugin."""

    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Configure Shortcut Composer")

        self._combo_boxes_layout = ComboBoxesLayout()
        self._spin_boxes_layout = SpinBoxesLayout()
        self._buttons_layout = ButtonsLayout(
            ok_callback=self._ok,
            apply_callback=self._apply,
            reset_callback=self._reset,
            cancel_callback=self.hide,
        )

        full_layout = QVBoxLayout()
        full_layout.addLayout(self._combo_boxes_layout)
        full_layout.addLayout(self._spin_boxes_layout)
        full_layout.addLayout(self._buttons_layout)
        self.setLayout(full_layout)

    def _apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        self._combo_boxes_layout.apply()
        self._spin_boxes_layout.apply()
        Krita.trigger_action("Reload Shortcut Composer")

    def _refresh(self) -> None:
        """Ask all dialog zones to refresh themselves. """
        self._combo_boxes_layout.refresh()
        self._spin_boxes_layout.refresh()

    def _ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self._apply()
        self.hide()

    def _reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        Config.reset_defaults()
        self._refresh()

    def show(self) -> None:
        """Show the dialog after refreshing all its elements."""
        self._refresh()
        self.move(QCursor.pos())
        return super().show()
