# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget

from api_krita.pyqt import AnimatedWidget, BaseWidget

from composer_utils import Config
from core_components import Controller
from .pie_style_holder import PieStyleHolder
from .pie_config import PieConfig
from .pie_settings_utils import PreferencesTab, LocationTab


class PieSettings(AnimatedWidget, BaseWidget):
    """
    Abstract widget that allows to change values in passed config.

    Meant to be displayed next to the pie menu when it enters edit mode.

    Consists of two obligatory tabs:
    - form with general configuration values.
    - tab for switching location in which values are saved.

    Subclasses can add their own tabs - they should do so with the tab
    with available values to drag into the pie.
    """

    def __init__(
        self,
        controller: Controller,
        config: PieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        AnimatedWidget.__init__(self, None, Config.PIE_ANIMATION_TIME.read())
        self.setMinimumHeight(round(style_holder.pie_style.widget_radius*2))
        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint))
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self._style_holder = style_holder
        self._config = config
        self._config.register_to_order_related(self._reset)

        self._tab_holder = QTabWidget()

        self._preferences_tab = PreferencesTab(
            self._config,
            controller.REQUIRES_TEXT_SETTINGS)

        self._tab_holder.addTab(self._preferences_tab, "Preferences")
        self._tab_holder.addTab(LocationTab(self._config), "Save location")

        layout = QVBoxLayout(self)
        layout.addWidget(self._tab_holder)
        self.setLayout(layout)

    def show(self) -> None:
        """Show the window after its settings are refreshed."""
        self._preferences_tab.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to kritarc."""
        self._preferences_tab.apply()
        super().hide()

    def _reset(self) -> None:
        """React to change in pie size."""
        self.setMinimumHeight(self._style_holder.pie_style.widget_radius*2)
