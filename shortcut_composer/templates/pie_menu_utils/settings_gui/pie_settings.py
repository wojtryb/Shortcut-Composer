# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout

from api_krita.pyqt import AnimatedWidget, BaseWidget, SafeConfirmButton
from config_system.ui import ConfigFormWidget, ConfigSpinBox
from composer_utils import Config
from ..pie_style import PieStyle
from ..pie_config import PieConfig


class PieSettings(AnimatedWidget, BaseWidget):
    """
    Abstract widget that allows to change values in passed config.

    Meant to be displayed next to pie menu, having the same heigth.
    """

    def __init__(
        self,
        config: PieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setMinimumHeight(round(style.widget_radius*2))
        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint))
        self.setCursor(Qt.ArrowCursor)

        self._style = style
        self._config = config
        self._config.register_callback(self._reset)

        self._tab_holder = QTabWidget()
        self._local_settings = ConfigFormWidget([
            ConfigSpinBox(config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(config.ICON_RADIUS_SCALE, self, "Icon max scale",
                          0.05, 4),
        ])
        self._tab_holder.addTab(self._local_settings, "Local settings")
        self._tab_holder.addTab(LocationTab(self._config), "Location")

        layout = QVBoxLayout(self)
        layout.addWidget(self._tab_holder)
        self.setLayout(layout)

    def show(self):
        """Show the window after its settings are refreshed."""
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to kritarc."""
        self._local_settings.apply()
        super().hide()

    def move_to_pie_side(self):
        """Move the widget on the right side of the pie."""
        offset = self.width()//2 + self._style.widget_radius * 1.05
        point = QPoint(round(offset), 0)
        # HACK Assume the pie center should be at the cursor
        self.move_center(QCursor().pos() + point)  # type: ignore

    def _reset(self):
        """React to change in pie size."""
        self.setMinimumHeight(self._style.widget_radius*2)


class LocationTab(QWidget):
    def __init__(
        self,
        config: PieConfig,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self._config = config

        self.location_button = self._init_location_button()
        self.reset_default_button = self._init_reset_button()

        layout = QVBoxLayout()
        layout.addWidget(self.location_button)
        layout.addWidget(self.reset_default_button)
        layout.addStretch()
        self.setLayout(layout)

        self.location_mode = self._config.SAVE_LOCAL.read()

    def _init_location_button(self):
        def switch_mode():
            self.location_mode = not self.location_mode

        location_button = SafeConfirmButton(confirm_text="Change?")
        location_button.clicked.connect(switch_mode)
        location_button.setFixedHeight(location_button.sizeHint().height()*2)
        return location_button

    def _init_reset_button(self):
        reset_button = SafeConfirmButton(text="Set current as default.")
        reset_button.clicked.connect(self._config.set_current_as_default)
        reset_button.setFixedHeight(reset_button.sizeHint().height()*2)
        return reset_button

    @property
    def location_mode(self):
        return self._config.SAVE_LOCAL.read()

    @location_mode.setter
    def location_mode(self, value: bool):
        if value:
            self.location_button.main_text = "Local mode"
            self._config.refresh_order()  # check if it is needed
            self._config.set_current_as_default()
        else:
            self.location_button.main_text = "Global mode"
        self._config.SAVE_LOCAL.write(value)
