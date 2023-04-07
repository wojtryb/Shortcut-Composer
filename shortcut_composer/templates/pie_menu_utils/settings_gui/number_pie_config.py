from typing import Optional

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from config_system.ui import ConfigFormWidget, ConfigSpinBox
from ..pie_config import NonPresetPieConfig
from ..pie_style import PieStyle
from .pie_settings import PieSettings


class NumberPieSettings(PieSettings):
    def __init__(
        self,
        config: NonPresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)

        self._local_settings = ConfigFormWidget([
            ConfigSpinBox(
                config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                config.ICON_RADIUS_SCALE, self, "Icon scale", 0.05, 4),
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
