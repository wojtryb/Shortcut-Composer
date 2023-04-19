# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional, Iterable

from PyQt5.QtWidgets import QWidget

from config_system import Field
from config_system.ui import ConfigComboBox
from core_components.controllers import PresetController
from data_components import Tag
from api_krita import Krita
from api_krita.wrappers import Database
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea


class TagComboBox(ConfigComboBox):
    """
    Combobox for picking preset tags, which can be saved in config.

    When `allow_all` flag is True, the combobox will contain "All" item
    will be added above the actual tags.
    """

    def __init__(
        self,
        config_field: Field[str],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        allow_all: bool = False,
    ) -> None:
        self._allow_all = allow_all
        self._preset_tags = []

        super().__init__(config_field, parent, pretty_name, self._preset_tags)

        self.refresh()
        self.reset()

    def refresh(self):
        """Replace list of available tags with those red from database."""
        self._preset_tags.clear()
        with Database() as database:
            self._preset_tags.extend(sorted(
                database.get_brush_tags(), key=str.lower))

        self.widget.clear()
        if self._allow_all:
            self.widget.addItem("All")
        self.widget.addItems(self._preset_tags)


class PresetScrollArea(ScrollArea):
    """
    Scroll area for holding preset pies.

    Extends usual scroll area with the bar over the area for picking
    displayed tag. The picked tag is saved to configuration.
    """

    def __init__(
        self,
        style: PieStyle,
        columns: int,
        config: PresetPieConfig,
        parent=None
    ) -> None:
        super().__init__(style, columns, parent)
        self._field = config.LAST_TAG_SELECTED
        self._tag_chooser = TagComboBox(self._field, allow_all=True)
        self._tag_chooser.widget.currentTextChanged.connect(
            self._change_handled_tag)
        self._layout.insertWidget(0, self._tag_chooser.widget)
        self._change_handled_tag()

    def _change_handled_tag(self):
        """Get newly set tag, create it's labels and update widgets."""
        picked_tag = self._tag_chooser.widget.currentText()
        if picked_tag == "All":
            values = Krita.get_presets().keys()
        else:
            values = Tag(picked_tag)

        labels = self._create_labels(values)
        self.replace_handled_labels(labels)
        self._apply_search_bar_filter()
        self._tag_chooser.save()

    def _create_labels(self, values: Iterable[str]):
        """Create labels from list of preset names."""
        controller = PresetController()
        labels: List[Label[str]] = []
        for preset_name in values:
            label = Label.from_value(preset_name, controller)
            if label is not None:
                labels.append(label)
        return labels


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

        self._action_values = PresetScrollArea(self._style, 3, config)
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
