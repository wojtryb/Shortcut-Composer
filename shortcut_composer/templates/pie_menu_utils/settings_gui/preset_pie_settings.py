# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Iterable

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
        super().__init__(config_field, parent, pretty_name)

    def reset(self):
        """Replace list of available tags with those red from database."""
        self._combo_box.clear()
        if self._allow_all:
            self._combo_box.addItem("All")
        with Database() as database:
            self._combo_box.addItems(database.get_brush_tags())
        self.set(self.config_field.read())


class PresetScrollArea(ScrollArea):
    """
    Scroll area for holding preset pies.

    Extends usual scroll area with the combobox over the area for
    picking displayed tag. The picked tag is saved to given field.
    """

    def __init__(
        self,
        style: PieStyle,
        columns: int,
        field: Field,
        parent=None
    ) -> None:
        super().__init__(style, columns, parent)
        self._field = field
        self.tag_chooser = TagComboBox(self._field, allow_all=True)
        self.tag_chooser.widget.currentTextChanged.connect(self._display_tag)
        self._layout.insertWidget(0, self.tag_chooser.widget)
        self._display_tag()

    def _display_tag(self):
        """Update preset widgets according to tag selected in combobox."""
        picked_tag = self.tag_chooser.widget.currentText()
        if picked_tag == "All":
            presets = Krita.get_presets().keys()
        else:
            presets = Tag(picked_tag)

        self.replace_handled_labels(self._create_labels(presets))
        self._apply_search_bar_filter()
        self.tag_chooser.save()

    def _create_labels(self, values: Iterable[str]):
        """Create labels from list of preset names."""
        controller = PresetController()
        labels = [Label.from_value(preset, controller) for preset in values]
        return [label for label in labels if label is not None]


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

        self._action_values = PresetScrollArea(
            style=self._style,
            columns=3,
            field=self._config.field("Last tag selected", "All"))
        self.retain_size_policy(self._action_values, True)

        def refresh_draggable():
            """Make all values used in pie undraggable and disabled."""
            self._action_values.mark_used_values(self._config.values())

        self._config.ORDER.register_callback(refresh_draggable)
        self._action_values.reloaded_signal.connect(refresh_draggable)
        refresh_draggable()

        self._mode_button = SafeConfirmButton()
        self._mode_button.clicked.connect(self._switch_is_tag_mode)
        self._mode_button.setFixedHeight(
            self._mode_button.sizeHint().height()*2)

        def save_picked_tag():
            self._auto_combobox.save()
            self._config.refresh_order()

        self._auto_combobox = TagComboBox(config.TAG_NAME, self, "Tag name")
        self._auto_combobox.widget.currentTextChanged.connect(save_picked_tag)

        self._manual_combobox = self._action_values.tag_chooser
        top_layout = QHBoxLayout()
        top_layout.addWidget(self._mode_button, 1)
        top_layout.addWidget(self._auto_combobox.widget, 2)
        top_layout.addWidget(self._manual_combobox.widget, 2)

        action_layout = QVBoxLayout()
        action_layout.addLayout(top_layout)
        action_layout.addWidget(self._action_values)
        action_layout.addStretch()

        tab_widget = QWidget()
        tab_widget.setLayout(action_layout)
        self._tab_holder.addTab(tab_widget, "Action values")

        self._set_is_tag_mode(self._config.IS_TAG_MODE.read())

    def _set_is_tag_mode(self, value: bool):
        """Set if presets should be picked from tag or by free picking."""
        self._config.IS_TAG_MODE.write(value)
        self._config.refresh_order()
        if value:
            # moving to tag mode
            self._mode_button.main_text = "Tag mode"
            self._action_values.hide()
            self._manual_combobox.widget.hide()
            self._auto_combobox.widget.show()
        else:
            # moving to manual mode
            self._mode_button.main_text = "Manual mode"
            self._action_values.show()
            self._manual_combobox.widget.show()
            self._auto_combobox.widget.hide()

    def _switch_is_tag_mode(self):
        """Change the is_tag_mode to the opposite state."""
        value = not self._config.IS_TAG_MODE.read()
        self._set_is_tag_mode(value)
        if value:
            self._auto_combobox.set(self._manual_combobox.read())
            self._auto_combobox.save()
        else:
            self._manual_combobox.set(self._auto_combobox.read())
            self._manual_combobox.save()

    @staticmethod
    def retain_size_policy(widget: QWidget, value: bool):
        """Make widget keep its place, when hidden."""
        policy = widget.sizePolicy()
        policy.setRetainSizeWhenHidden(value)
        widget.setSizePolicy(policy)
