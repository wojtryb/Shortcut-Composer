# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget

from api_krita.pyqt import AnimatedWidget, BaseWidget
from api_krita.enums.helpers import EnumGroup
from composer_utils import Config
from composer_utils.label.complex_widgets import NumericValuePicker
from core_components import Controller, NumericController
from .pie_config import PieConfig
from .pie_label import PieLabel
from .pie_settings_tabs import TabPreferences, TabValuesList, TabSaveLocation
from .pie_style_holder import PieStyleHolder
from .pie_widget_utils import PieWidgetOrder


class PieSettings(AnimatedWidget, BaseWidget):
    """
    Widget that allows to change values in passed config.

    Meant to be displayed next to the pie menu when it enters edit mode.

    Consists of tabs, that may depend on the passed controller:
    - preferences - form with general configuration values.
    - values - (depends on controller) allows to change values in pie.
    - save location - allows to save values in .kritarc or in .kra.

    Refreshes settings on show, and applies them on hide.
    """

    def __init__(
        self,
        controller: Controller,
        config: PieConfig,
        style_holder: PieStyleHolder,
        order_handler: PieWidgetOrder,
    ) -> None:
        AnimatedWidget.__init__(
            self,
            animation_time_s=Config.PIE_ANIMATION_TIME.read(),
            fps_limit=Config.FPS_LIMIT.read())

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint))
        self.setCursor(Qt.CursorShape.ArrowCursor)

        self._tab_holder = QTabWidget()

        # First tab
        self._preferences_tab = TabPreferences(
            config=config,
            requires_text_settings=controller.REQUIRES_TEXT_SETTINGS)
        self._tab_holder.addTab(self._preferences_tab, "Preferences")

        # Second tab (optional, depend on controller type)
        if issubclass(controller.TYPE, (str, EnumGroup)):
            tab = TabValuesList(
                config=TabValuesList.Config(
                    config.GROUP_MODE,
                    config.GROUP_NAME,
                    config.LAST_GROUP_SELECTED),
                order_handler=order_handler,
                controller=controller,
                label_style=style_holder.settings_label_style)
            self._tab_holder.addTab(tab, "Values")
            self._tab_holder.setCurrentIndex(1)
        elif isinstance(controller, NumericController):
            def label_from_integer(value: int) -> PieLabel[int]:
                label = PieLabel.from_value(value, controller)
                if label is None:
                    raise RuntimeError(f"Could not create label from {value}")
                return label

            tab = NumericValuePicker(
                create_label_from_integer=label_from_integer,
                unscaled_label_style=style_holder.settings_label_style,
                min_value=controller.MIN_VALUE,
                max_value=controller.MAX_VALUE,
                step=controller.STEP,
                wrapping=controller.WRAPPING,
                adaptive=controller.ADAPTIVE)
            self._tab_holder.addTab(tab, "Values")
            self._tab_holder.setCurrentIndex(1)

        # Third tab
        tab = TabSaveLocation(config, order_handler, controller)
        self._tab_holder.addTab(tab, "Save location")

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
