# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional
from enum import Enum

from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget

from core_components import Controller
from config_system.ui import ConfigFormWidget, ConfigSpinBox
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import NonPresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea


class EnumPieSettings(PieSettings):
    """
    Pie setting window for pie values being enums.

    Consists of two tabs:
    - usual form with field values to set
    - scrollable area with all available enum values to drag into pie
    """

    def __init__(
        self,
        controller: Controller[Enum],
        used_values: List[Label],
        config: NonPresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)

        self._used_values = used_values

        names = controller.TYPE._member_names_
        values = [controller.TYPE[name] for name in names]
        labels = [Label.from_value(value, controller) for value in values]
        labels = [label for label in labels if label is not None]

        tab_holder = QTabWidget()

        self._action_values = ScrollArea(self._style, 3)
        self._action_values.replace_handled_labels(labels)
        self._action_values.setMinimumHeight(
            round(style.unscaled_icon_radius*6.2))

        tab_holder.addTab(self._action_values, "Action values")
        self._local_settings = ConfigFormWidget([
            ConfigSpinBox(config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                config.ICON_RADIUS_SCALE, self, "Icon max scale",  0.05, 4),
        ])
        tab_holder.addTab(self._local_settings, "Local settings")

        layout = QVBoxLayout(self)
        layout.addWidget(tab_holder)
        self.setLayout(layout)

        self._config.ORDER.register_callback(self.refresh)
        self.refresh()

    def refresh(self):
        """Make all values currently used in pie undraggable and disabled."""
        for widget in self._action_values.children_list:
            if widget.label in self._used_values:
                widget.enabled = False
                widget.draggable = False
            else:
                widget.enabled = True
                widget.draggable = True

    def show(self):
        """Show the window after its settings are refreshed."""
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to kritarc."""
        self._local_settings.apply()
        super().hide()
