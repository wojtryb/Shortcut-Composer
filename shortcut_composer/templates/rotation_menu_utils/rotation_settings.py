# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.pyqt import BaseWidget

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout

from composer_utils import ButtonsLayout
from config_system.ui import (
    ConfigFormWidget,
    EnumComboBox,
    ColorButton,
    Checkbox,
    SpinBox)
from data_components import RotationDeadzoneStrategy
from .rotation_config import RotationConfig


class RotationSettings(BaseWidget):
    """Widget that allows to change values in passed config."""

    def __init__(self, config: RotationConfig) -> None:
        super().__init__(None)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)  # type: ignore

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle(f"Settings: {config.name}")

        self._config = config

        self._general_tab = ConfigFormWidget([
            "Behavior",
            EnumComboBox(
                config_field=config.DEADZONE_STRATEGY,
                parent=self,
                pretty_name="On deadzone",
                enum_type=RotationDeadzoneStrategy),
            Checkbox(
                config_field=config.INVERSE_ZONES,
                parent=self,
                pretty_name="Inverse zones"),
            SpinBox(
                config_field=config.DIVISIONS,
                parent=self,
                pretty_name="Divisions",
                step=1,
                max_value=360),

            "Size",
            SpinBox(
                config_field=config.DEADZONE_SCALE,
                parent=self,
                pretty_name="Deadzone scale",
                step=0.05,
                max_value=4),
            SpinBox(
                config_field=config.INNER_ZONE_SCALE,
                parent=self,
                pretty_name="Inner zone scale",
                step=0.05,
                max_value=4),

            "Style",
            ColorButton(
                config_field=config.ACTIVE_COLOR,
                parent=self,
                pretty_name="Active color"),
            SpinBox(
                config_field=config.OUTLINE_OPACITY,
                parent=self,
                pretty_name="Outline opacity",
                step=1,
                max_value=255),

            "Values",
            Checkbox(
                config_field=config.IS_COUNTERCLOCKWISE,
                parent=self,
                pretty_name="Is counterclockwise"),
            SpinBox(
                config_field=config.OFFSET,
                parent=self,
                pretty_name="Offset",
                step=1,
                max_value=360),
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
        self.move_center(QCursor.pos())
        return super().show()

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        self._general_tab.apply()

    def ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self.apply()
        self.hide()

    def reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        self._config.reset_default()
        self.refresh()

    def refresh(self) -> None:
        """Update boxes with configured values."""
        self._general_tab.refresh()
