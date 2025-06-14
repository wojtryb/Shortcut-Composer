# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from composer_utils.label.complex_widgets import ScrollArea
from core_components.controllers import PresetController
from templates.pie_menu_utils import PieSettings, PieConfig
from ..pie_style_holder import PieStyleHolder
from ..group_manager_impl import dispatch_group_manager
from .common_utils import GroupComboBox


class PresetPieSettings(PieSettings):
    """
    Pie setting window for pie values being brush presets.

    Its `Values` tab operates in two modes:
    - Tag mode - the presets are determined by tracking krita tag
    - Manual mode - the presets are manually picked by the user
    """

    def __init__(
        self,
        controller: PresetController,
        config: PieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        super().__init__(controller, config, style_holder)
        self._config: PieConfig

        self._manager = dispatch_group_manager(controller)
        self._scroll_area = self._init_scroll_area()
        self._mode_button = self._init_mode_button()
        self._auto_combobox = self._init_auto_combobox()
        self._manual_combobox = self._init_manual_combobox()

        self.set_tag_mode(self._config.TAG_MODE.read())
        action_values = self._init_action_values()
        self._tab_holder.insertTab(1, action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

    def _init_scroll_area(self) -> ScrollArea:
        """Create preset scroll area which tracks which ones are used."""
        scroll_area = ScrollArea(
            label_style=self._style_holder.settings_label_style,
            columns=3)
        policy = scroll_area.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        scroll_area.setSizePolicy(policy)

        def refresh_draggable() -> None:
            """Mark which pies are currently used in the pie."""
            scroll_area.mark_used_values(self._config.values())

        self._config.ORDER.register_callback(refresh_draggable)
        scroll_area.widgets_changed.connect(refresh_draggable)
        refresh_draggable()
        return scroll_area

    def _init_mode_button(self) -> SafeConfirmButton:
        """Create button which switches between tag and manual mode."""
        def switch_mode() -> None:
            """Change the is_tag_mode to the opposite state."""
            is_tag_mode = not self.get_tag_mode()
            self.set_tag_mode(is_tag_mode)
            if is_tag_mode:
                self._auto_combobox.set(self._manual_combobox.read())
                self._auto_combobox.save()
                # Reset hidden combobox to prevent unnecessary icon loading
                self._manual_combobox.set(
                    self._manual_combobox.config_field.default)
                self._manual_combobox.save()
            else:
                self._manual_combobox.set(self._auto_combobox.read())
                self._manual_combobox.save()

        mode_button = SafeConfirmButton(confirm_text="Change?")
        mode_button.clicked.connect(switch_mode)
        mode_button.setFixedHeight(mode_button.sizeHint().height()*2)
        self._config.TAG_MODE.register_callback(
            lambda: self.set_tag_mode(self._config.TAG_MODE.read(), False))
        return mode_button

    def _init_auto_combobox(self) -> GroupComboBox:
        """Create tag mode combobox, which sets tag presets to the pie."""
        def handle_picked_tag() -> None:
            """Save used tag in config and report the values changed."""
            auto_combobox.save()
            self._config.refresh_order()

        auto_combobox = GroupComboBox(
            last_value_field=self._config.TAG_NAME,
            group_manager=self._manager,
            pretty_name="Tag name")

        auto_combobox.widget.currentTextChanged.connect(handle_picked_tag)
        return auto_combobox

    def _init_manual_combobox(self) -> GroupComboBox:
        def _display_group() -> None:
            """Update preset widgets according to tag selected in combobox."""
            picked_group = manual_combobox.widget.currentText()
            values = self._manager.get_values(picked_group)
            self._scroll_area.replace_handled_labels(
                self._manager.create_labels(values))
            self._scroll_area._apply_search_bar_filter()
            manual_combobox.save()

        manual_combobox = GroupComboBox(
            last_value_field=self._config.LAST_TAG_SELECTED,
            group_manager=self._manager,
            additional_fields=["---Select tag---", "All"])

        manual_combobox.widget.currentTextChanged.connect(_display_group)
        _display_group()

        return manual_combobox

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
        # Do not display picker, when there is only one group
        if len(self._manager.fetch_groups()) <= 1:
            self._mode_button.hide()
            self._auto_combobox.widget.hide()
            self._manual_combobox.widget.hide()

        action_layout = QVBoxLayout()
        action_layout.addLayout(top_layout)
        action_layout.addWidget(self._scroll_area)
        action_layout.addStretch()

        action_values_tab = QWidget()
        action_values_tab.setLayout(action_layout)
        return action_values_tab

    def get_tag_mode(self) -> bool:
        """Return whether pie is in tag mode or not (manual mode)."""
        return self._config.TAG_MODE.read()

    def set_tag_mode(self, value: bool, notify: bool = True) -> None:
        """Set the pie mode to tag (True) or manual (False)."""
        if notify:
            self._config.TAG_MODE.write(value)
        self._config.refresh_order()
        if value:
            # moving to tag mode
            self._mode_button.main_text = "Tag mode"
            self._mode_button.icon = Krita.get_icon("tag")
            self._scroll_area.hide()
            self._manual_combobox.widget.hide()
            self._auto_combobox.widget.show()
        else:
            # moving to manual mode
            self._mode_button.main_text = "Manual mode"
            self._mode_button.icon = Krita.get_icon("color-to-alpha")
            self._scroll_area.show()
            self._manual_combobox.widget.show()
            self._auto_combobox.widget.hide()
