from typing import List

from PyQt5.QtWidgets import QVBoxLayout
from api_krita.wrappers import Database
from config_system.ui import (
    ConfigFormWidget,
    ConfigComboBox,
    ConfigSpinBox)
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings


class PresetPieSettings(PieSettings):
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
            style,
            pie_config,
            parent)

        self._tags: List[str] = []
        self._refresh_tags()

        self._local_settings = ConfigFormWidget([
            ConfigComboBox(pie_config.TAG_NAME, self, "Tag name", self._tags),
            ConfigSpinBox(
                pie_config.PIE_RADIUS_SCALE, self, "Pie scale", 0.05, 4),
            ConfigSpinBox(
                pie_config.ICON_RADIUS_SCALE, self, "Icon scale", 0.05, 4),
        ])

        layout = QVBoxLayout(self)
        layout.addWidget(self._local_settings)
        self.setLayout(layout)

    def show(self):
        self._refresh_tags()
        self._local_settings.refresh()
        super().show()

    def hide(self) -> None:
        self._local_settings.apply()
        super().hide()

    def _refresh_tags(self):
        with Database() as database:
            tags = sorted(database.get_brush_tags(), key=str.lower)
        self._tags.clear()
        self._tags.extend(tags)
