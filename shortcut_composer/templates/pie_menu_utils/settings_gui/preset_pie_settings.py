# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from api_krita.wrappers import Database
from config_system.ui import (
    ConfigFormWidget,
    ConfigComboBox,
    ConfigSpinBox)
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings


class PresetPieSettings(PieSettings):
    """Pie setting window for pie values being brush presets."""

    def __init__(
        self,
        config: PresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)

        self._tags: List[str] = []
        self._refresh_tags()

        self._local_settings = ConfigFormWidget([
            ConfigComboBox(config.TAG_NAME, self, "Tag name", self._tags),
            ConfigSpinBox(config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                config.ICON_RADIUS_SCALE, self, "Icon scale", 0.05, 4),
        ])

        layout = QVBoxLayout(self)
        layout.addWidget(self._local_settings)
        self.setLayout(layout)

    def show(self):
        """Show the window after its settings are refreshed."""
        self._refresh_tags()
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to .kritarc."""
        self._local_settings.apply()
        super().hide()

    def _refresh_tags(self):
        """Replace list of available tags with those red from database."""
        self._tags.clear()
        with Database() as database:
            self._tags.extend(sorted(database.get_brush_tags(), key=str.lower))
