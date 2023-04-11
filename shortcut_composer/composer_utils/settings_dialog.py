# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor

from INFO import __version__, __author__, __license__
from api_krita import Krita
from config_system.ui import ConfigFormWidget, ConfigSpinBox
from .global_config import Config
from .buttons_layout import ButtonsLayout


class SettingsDialog(QDialog):
    """Dialog which allows to configure plugin elements."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)  # type: ignore

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Configure Shortcut Composer")

        self._general_tab = ConfigFormWidget([
            "Common settings",
            ConfigSpinBox(
                Config.SHORT_VS_LONG_PRESS_TIME, self, None, 0.05, 4),
            ConfigSpinBox(Config.FPS_LIMIT, self, None, 5, 500),
            "Cursor trackers",
            ConfigSpinBox(
                Config.TRACKER_SENSITIVITY_SCALE, self, None, 0.05, 400),
            ConfigSpinBox(Config.TRACKER_DEADZONE, self, None, 1, 200),
            "Pie menus display",
            ConfigSpinBox(Config.PIE_GLOBAL_SCALE, self, None, 0.05, 4),
            ConfigSpinBox(Config.PIE_ICON_GLOBAL_SCALE, self, None, 0.05, 4),
            ConfigSpinBox(
                Config.PIE_DEADZONE_GLOBAL_SCALE, self, None, 0.05, 4),
            ConfigSpinBox(Config.PIE_ANIMATION_TIME, self, None, 0.01, 1),
            f"Shortcut Composer v{__version__}\n"
            f"Maintainer: {__author__}\n"
            f"License: {__license__}",
        ])

        full_layout = QVBoxLayout(self)
        full_layout.addWidget(self._general_tab)
        full_layout.addLayout(ButtonsLayout(
            ok_callback=self.ok,
            apply_callback=self.apply,
            reset_callback=self.reset,
            cancel_callback=self.hide,
        ))
        self.setLayout(full_layout)

    def show(self) -> None:
        """Show the dialog after refreshing all its elements."""
        self.refresh()
        self.move(QCursor.pos())
        return super().show()

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        self._general_tab.apply()
        Krita.trigger_action("Reload Shortcut Composer")

    def ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self.apply()
        self.hide()

    def reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        Config.reset_default()
        self.refresh()
        Krita.trigger_action("Reload Shortcut Composer")

    def refresh(self):
        self._general_tab.refresh()
