# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor

from api_krita import Krita
from INFO import __version__, __author__, __license__
from config_system.ui import ConfigFormWidget, SpinBox, ColorButton, Checkbox
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
            SpinBox(
                config_field=Config.SHORT_VS_LONG_PRESS_TIME,
                parent=self,
                pretty_name="Short vs long press time",
                step=0.05,
                max_value=4),
            SpinBox(
                config_field=Config.FPS_LIMIT,
                parent=self,
                pretty_name="FPS limit",
                step=5,
                max_value=50),

            "Cursor trackers",
            SpinBox(
                Config.TRACKER_SENSITIVITY_SCALE,
                parent=self,
                pretty_name="Tracker sensitivity scale",
                step=0.05,
                max_value=400),
            SpinBox(
                Config.TRACKER_DEADZONE,
                parent=self,
                pretty_name="Tracker deadzone",
                step=1,
                max_value=20),

            "Pie menu size",
            SpinBox(
                Config.PIE_GLOBAL_SCALE,
                parent=self,
                pretty_name="Pie global scale",
                step=0.05,
                max_value=4),
            SpinBox(
                Config.PIE_ICON_GLOBAL_SCALE,
                parent=self,
                pretty_name="Pie icon global scale",
                step=0.05,
                max_value=4),
            SpinBox(
                Config.PIE_DEADZONE_GLOBAL_SCALE,
                parent=self,
                pretty_name="Pie deadzone global scale",
                step=0.05,
                max_value=4),

            "Pie menu style",
            bg_checkbox := Checkbox(
                config_field=Config.OVERRIDE_BACKGROUND_THEME_COLOR,
                parent=self,
                pretty_name="Override background theme color"),
            bg_button := ColorButton(
                config_field=Config.DEFAULT_BACKGROUND_COLOR,
                parent=self,
                pretty_name="Default background color"),
            active_checkbox := Checkbox(
                config_field=Config.OVERRIDE_ACTIVE_THEME_COLOR,
                parent=self,
                pretty_name="Override active theme color"),
            active_button := ColorButton(
                config_field=Config.DEFAULT_ACTIVE_COLOR,
                parent=self,
                pretty_name="Default active color"),
            SpinBox(
                config_field=Config.DEFAULT_PIE_OPACITY,
                parent=self,
                pretty_name="Default pie opacity",
                step=1,
                max_value=100),
            SpinBox(
                config_field=Config.PIE_ANIMATION_TIME,
                parent=self,
                pretty_name="Pie animation time",
                step=0.01,
                max_value=1),

            f"Shortcut Composer v{__version__}\n"
            f"Maintainer: {__author__}\n"
            f"License: {__license__}",
        ])

        def update_theme_state():
            """Hide color buttons when not taken into consideration."""
            bg_button.widget.setVisible(bg_checkbox.widget.isChecked())
            active_button.widget.setVisible(active_checkbox.widget.isChecked())
        bg_checkbox.widget.stateChanged.connect(update_theme_state)
        active_checkbox.widget.stateChanged.connect(update_theme_state)
        update_theme_state()

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

    def refresh(self) -> None:
        self._general_tab.refresh()
