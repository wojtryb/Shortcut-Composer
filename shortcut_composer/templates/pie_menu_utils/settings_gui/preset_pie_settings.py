# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget

from core_components.controllers import PresetController
from api_krita import Krita
from api_krita.wrappers import Database
from config_system.ui import (
    ConfigFormWidget,
    ConfigComboBox,
    ConfigSpinBox)
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea


class PresetPieSettings(PieSettings):
    """Pie setting window for pie values being brush presets."""

    def __init__(
        self,
        used_values: List[Label],
        config: PresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)

        self._used_values = used_values
        self._tags: List[str] = []

        tab_holder = QTabWidget()

        controller = PresetController()
        values: List[Label[str]] = []
        for preset_name in Krita.get_presets().keys():
            label = Label.from_value(preset_name, controller)
            if label is not None:
                values.append(label)

        self._action_values = ScrollArea(self._style, 3)
        self._action_values.replace_handled_labels(values)
        self._action_values.setMinimumHeight(
            round(style.unscaled_icon_radius*6.2))

        tab_holder.addTab(self._action_values, "Action values")
        self._local_settings = ConfigFormWidget([
            ConfigComboBox(config.TAG_NAME, self, "Tag name", self._tags),
            ConfigSpinBox(config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                config.ICON_RADIUS_SCALE, self, "Icon max scale", 0.05, 4),
        ])
        tab_holder.addTab(self._local_settings, "Local settings")

        self._refresh_tags()
        self._refresh_draggable()

        layout = QVBoxLayout(self)
        layout.addWidget(tab_holder)
        self.setLayout(layout)

    def show(self):
        """Show the window after its settings are refreshed."""
        self._refresh_tags()
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to kritarc."""
        self._local_settings.apply()
        super().hide()

    def _refresh_tags(self):
        """Replace list of available tags with those red from database."""
        self._tags.clear()
        with Database() as database:
            self._tags.extend(sorted(database.get_brush_tags(), key=str.lower))

    def _refresh_draggable(self):
        """Make all values currently used in pie undraggable and disabled."""
        for widget in self._action_values.children_list:
            if widget.label in self._used_values:
                widget.enabled = False
                widget.draggable = False
            else:
                widget.enabled = True
                widget.draggable = True
