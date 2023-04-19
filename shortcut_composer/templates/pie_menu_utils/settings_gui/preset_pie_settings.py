# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from PyQt5.QtWidgets import QWidget

from core_components.controllers import PresetController
from config_system import Field
from config_system.ui import ConfigComboBox
from api_krita import Krita
from api_krita.wrappers import Database
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea


class TagComboBox(ConfigComboBox):
    def __init__(
        self,
        config_field: Field[str],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
    ) -> None:
        self._preset_tags = []
        self.refresh()
        super().__init__(config_field, parent, pretty_name, self._preset_tags)

    def refresh(self):
        """Replace list of available tags with those red from database."""
        self._preset_tags.clear()
        with Database() as database:
            self._preset_tags.extend(sorted(
                database.get_brush_tags(), key=str.lower))


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

        controller = PresetController()
        labels: List[Label[str]] = []
        for preset_name in Krita.get_presets().keys():
            label = Label.from_value(preset_name, controller)
            if label is not None:
                labels.append(label)

        self._action_values = ScrollArea(self._style, 3)
        self._action_values.replace_handled_labels(labels)
        self._action_values.setMinimumHeight(
            round(style.unscaled_icon_radius*6.2))
        self._tab_holder.addTab(self._action_values, "Action values")

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self):
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_labels(self._used_values)

# tag_combo = TagComboBox(config.TAG_NAME, self, "Tag name"),
# tag_combo.refresh()
