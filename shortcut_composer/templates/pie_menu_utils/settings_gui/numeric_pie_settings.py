# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from config_system.ui import ConfigFormWidget, ConfigSpinBox
from ..pie_config import NonPresetPieConfig
from ..pie_style import PieStyle
from .pie_settings import PieSettings


class NumericPieSettings(PieSettings):
    """Pie setting window for pie values being numeric (float or int)."""

    def __init__(
        self,
        config: NonPresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)

        self._local_settings = ConfigFormWidget([
            ConfigSpinBox(config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                config.ICON_RADIUS_SCALE, self, "Icon scale", 0.05, 4),
        ])

        layout = QVBoxLayout(self)
        layout.addWidget(self._local_settings)
        self.setLayout(layout)

    def show(self):
        """Show the window after its settings are refreshed."""
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        """Hide the window after its settings are saved to .kritarc."""
        self._local_settings.apply()
        super().hide()
