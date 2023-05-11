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
        self.config_field.register_callback(
            lambda: self.set(self.config_field.read()))

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

    Operates in two modes:
    - Tag mode - the presets are determined by tracking krita tag
    - Manual mode - the presets are manually picked by the user
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

        self._preset_scroll_area = self._init_preset_scroll_area()
        self._mode_button = self._init_mode_button()
        self._auto_combobox = self._init_auto_combobox()
        self._manual_combobox = self._preset_scroll_area.tag_chooser

        self.set_tag_mode(self._config.TAG_MODE.read())
        action_values = self._init_action_values()
        self._tab_holder.insertTab(1, action_values, "Action values")
        self._tab_holder.setCurrentIndex(1)

    def _init_preset_scroll_area(self) -> PresetScrollArea:
        """Create preset scroll area which tracks which ones are used."""
        preset_scroll_area = PresetScrollArea(
            style=self._style,
            columns=3,
            field=self._config.field("Last tag selected", "All"))
        policy = preset_scroll_area.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        preset_scroll_area.setSizePolicy(policy)

        def refresh_draggable():
            """Mark which pies are currently used in the pie."""
            preset_scroll_area.mark_used_values(self._config.values())

        self._config.ORDER.register_callback(refresh_draggable)
        preset_scroll_area.widgets_changed.connect(refresh_draggable)
        refresh_draggable()
        return preset_scroll_area

    def _init_mode_button(self) -> SafeConfirmButton:
        """Create button which switches between tag and manual mode."""
        def switch_mode():
            """Change the is_tag_mode to the opposite state."""
            new_value = not self.get_tag_mode()
            self.set_tag_mode(new_value)
            if new_value:
                self._auto_combobox.set(self._manual_combobox.read())
                self._auto_combobox.save()
            else:
                self._manual_combobox.set(self._auto_combobox.read())
                self._manual_combobox.save()

        mode_button = SafeConfirmButton(confirm_text="Change?")
        mode_button.clicked.connect(switch_mode)
        mode_button.setFixedHeight(mode_button.sizeHint().height()*2)
        self._config.TAG_MODE.register_callback(
            lambda: self.set_tag_mode(self._config.TAG_MODE.read(), False))
        return mode_button

    def _init_auto_combobox(self) -> TagComboBox:
        """Create tag modecombobox, which sets tag presets to the pie."""
        def handle_picked_tag():
            """Save used tag in config and report the values changed."""
            auto_combobox.save()
            self._config.refresh_order()

        auto_combobox = TagComboBox(self._config.TAG_NAME, self, "Tag name")
        auto_combobox.widget.currentTextChanged.connect(handle_picked_tag)
        return auto_combobox

    def _init_action_values(self) -> QWidget:
        """
        Create Action Values tab of the Settings Window.

        - Mode button and two comboboxes are places at the top
        - Below them lies the preset scroll area
        - Two comboboxes will swap with each other when the mode changes
        - Scroll area combobox is taken out of it, and placed with the
          other one to save space.
        """
        top_layout = QHBoxLayout()
        top_layout.addWidget(self._mode_button, 1)
        top_layout.addWidget(self._auto_combobox.widget, 2)
        top_layout.addWidget(self._manual_combobox.widget, 2)

        action_layout = QVBoxLayout()
        action_layout.addLayout(top_layout)
        action_layout.addWidget(self._preset_scroll_area)
        action_layout.addStretch()

        action_values_tab = QWidget()
        action_values_tab.setLayout(action_layout)
        return action_values_tab

    def get_tag_mode(self):
        """Return whether pie is in tag mode or not (manual mode)."""
        return self._config.TAG_MODE.read()

    def set_tag_mode(self, value: bool, notify: bool = True):
        """Set the pie mode to tag (True) or manual (False)."""
        if notify:
            self._config.TAG_MODE.write(value)
        self._config.refresh_order()
        if value:
            # moving to tag mode
            self._mode_button.main_text = "Tag mode"
            self._mode_button.icon = Krita.get_icon("tag")
            self._preset_scroll_area.hide()
            self._manual_combobox.widget.hide()
            self._auto_combobox.widget.show()
        else:
            # moving to manual mode
            self._mode_button.main_text = "Manual mode"
            self._mode_button.icon = Krita.get_icon("color-to-alpha")
            self._preset_scroll_area.show()
            self._manual_combobox.widget.show()
            self._auto_combobox.widget.hide()
