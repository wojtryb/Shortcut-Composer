from typing import List

from PyQt5.QtWidgets import QVBoxLayout
from config_system.ui import ConfigFormWidget, ConfigSpinBox
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings


class NumberPieSettings(PieSettings):
    def __init__(
        self,
        values: List[Label],
        used_values: List[Label],
        style: PieStyle,
        pie_config: PresetPieConfig,
        parent=None
    ) -> None:
        super().__init__(
            values,
            used_values,
            style,
            pie_config,
            parent)

        self._local_settings = ConfigFormWidget([
            ConfigSpinBox(
                pie_config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                pie_config.ICON_RADIUS_SCALE, self, "Icon scale", 0.05, 4),
        ])

        layout = QVBoxLayout(self)
        layout.addWidget(self._local_settings)
        self.setLayout(layout)

    def show(self):
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        self._local_settings.apply()
        super().hide()
