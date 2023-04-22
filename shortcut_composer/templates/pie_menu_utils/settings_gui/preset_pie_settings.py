# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional, Iterable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from config_system import Field
from config_system.ui import ConfigComboBox
from core_components.controllers import PresetController
from data_components import Tag
from api_krita import Krita
from api_krita.wrappers import Database
from api_krita.pyqt import SafeConfirmButton
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
        self.tag_chooser = TagComboBox(self._field, allow_all=True)
        self.tag_chooser.widget.currentTextChanged.connect(
            self._change_handled_tag)
        self._layout.insertWidget(0, self.tag_chooser.widget)
        self._change_handled_tag()

    def _change_handled_tag(self):
        """Get newly set tag, create it's labels and update widgets."""
        picked_tag = self.tag_chooser.widget.currentText()
        if picked_tag == "All":
            values = Krita.get_presets().keys()
        else:
            values = Tag(picked_tag)

        labels = self._create_labels(values)
        self.replace_handled_labels(labels)
        self._apply_search_bar_filter()
        self.tag_chooser.save()

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
        config: PresetPieConfig,
        style: PieStyle,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(config, style, parent)
        self._config: PresetPieConfig

        self._action_values = PresetScrollArea(self._style, 3, self._config)
        self.retain_size_policy(self._action_values, True)

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

        self._mode_switch_button = SafeConfirmButton()
        self._mode_switch_button.clicked.connect(self._switch_is_tag_mode)
        self._mode_switch_button.setFixedHeight(
            self._mode_switch_button.sizeHint().height()*2)
        self._tag_combobox = TagComboBox(config.TAG_NAME, self, "Tag name")
        self._tag_combobox.widget.currentTextChanged.connect(
            self._reset_preset_config)

        self._manual_tag_combobox = self._action_values.tag_chooser

        top_layout = QHBoxLayout()
        top_layout.addWidget(self._mode_switch_button, 1)
        top_layout.addWidget(self._tag_combobox.widget, 2)
        top_layout.addWidget(self._manual_tag_combobox.widget, 2)

        action_layout = QVBoxLayout()
        action_layout.addLayout(top_layout)
        action_layout.addWidget(self._action_values)
        action_layout.addStretch()
        tab_widget = QWidget()
        tab_widget.setLayout(action_layout)
        self._tab_holder.addTab(tab_widget, "Action values")

        self._set_is_tag_mode(self._config.IS_TAG_MODE.read())

    def _reset_preset_config(self):
        self._tag_combobox.save()
        self._save_order()

    def _save_order(self):
        self._config.ORDER.write(self._config.values())

    def _refresh_draggable(self):
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_values(self._config.values())

    def _set_is_tag_mode(self, value: bool):
        """Set if presets should be picked from tag or by free picking."""
        self._config.IS_TAG_MODE.write(value)
        self._save_order()
        if value:
            # moving to tag mode
            self._mode_switch_button.main_text = "Tag mode"
            self._action_values.hide()
            self._manual_tag_combobox.widget.hide()
            self._tag_combobox.widget.show()
        else:
            # moving to manual mode
            self._mode_switch_button.main_text = "Manual mode"
            self._action_values.show()
            self._manual_tag_combobox.widget.show()
            self._tag_combobox.widget.hide()

    def _switch_is_tag_mode(self):
        """Change the is_tag_mode to the opposite state."""
        value = not self._config.IS_TAG_MODE.read()
        self._set_is_tag_mode(value)
        if value:
            self._tag_combobox.set(self._manual_tag_combobox.read())
            self._tag_combobox.save()
        else:
            self._manual_tag_combobox.set(self._tag_combobox.read())
            self._manual_tag_combobox.save()

    def hide(self) -> None:
        """Save the picked tag when in tag mode."""
        if self._config.IS_TAG_MODE.read():
            self._tag_combobox.save()
        return super().hide()

    @staticmethod
    def retain_size_policy(widget: QWidget, value: bool):
        """Make widget keep its place, when hidden."""
        policy = widget.sizePolicy()
        policy.setRetainSizeWhenHidden(value)
        widget.setSizePolicy(policy)
