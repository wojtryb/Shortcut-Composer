from api_krita.pyqt import BaseWidget

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout

from composer_utils import ButtonsLayout
from .rotation_config import RotationConfig
from config_system.ui import (
    ConfigFormWidget,
    ColorButton,
    Checkbox,
    SpinBox)


class RotationSettings(BaseWidget):

    def __init__(self, config: RotationConfig) -> None:
        super().__init__(None)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowStaysOnTopHint)  # type: ignore

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle(f"Rotation settings: {config.name}")

        self._config = config

        config.DIVISIONS
        config.INVERSE_ZONES
        self._general_tab = ConfigFormWidget([
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

            "Behavior",
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

            "Style",
            ColorButton(
                config_field=config.ACTIVE_COLOR,
                parent=self,
                pretty_name="Active color"),
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

    def refresh(self):
        self._general_tab.refresh()
