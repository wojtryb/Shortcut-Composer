# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from config_system.ui import StringComboBox
from composer_utils import GroupOrderHolder
from composer_utils.label.complex_widgets import ScrollArea
from core_components import Controller
from ..pie_config import PieConfig
from ..pie_value_manager_impl import dispatch_pie_value_manager
from ..pie_style_holder import PieStyleHolder
from ..pie_widget_utils import PieWidgetOrder


class TabValuesList(QWidget):

    def __init__(
        self,
        config: PieConfig,
        order_handler: PieWidgetOrder,
        controller: Controller,
        style_holder: PieStyleHolder,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._order_handler = order_handler
        self._style_holder = style_holder

        self._group_order_holder = GroupOrderHolder(controller.TYPE)
        self._label_creator = dispatch_pie_value_manager(controller)
        self._scroll_area = self._init_scroll_area()
        self._mode_button = self._init_mode_button()
        self._auto_combobox = self._init_auto_combobox()
        self._manual_combobox = self._init_manual_combobox()

        self._set_tag_mode()
        self.setLayout(self._init_layout())

    def _init_layout(self) -> QVBoxLayout:
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
        if len(self._label_creator.fetch_groups()) <= 1:
            self._mode_button.hide()
            self._auto_combobox.widget.hide()
            self._manual_combobox.widget.hide()

        action_layout = QVBoxLayout()
        action_layout.addLayout(top_layout)
        action_layout.addWidget(self._scroll_area)
        action_layout.addStretch()

        return action_layout

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
            scroll_area.mark_used_values(self._order_handler.values)

        self._order_handler.register_callback_on_change(refresh_draggable)
        scroll_area.widgets_changed.connect(refresh_draggable)
        refresh_draggable()
        return scroll_area

    def _init_mode_button(self) -> SafeConfirmButton:
        """Create button which switches between tag and manual mode."""
        def switch_mode() -> None:
            """Change the is_tag_mode to the opposite state."""
            # Writing to TAG_MODE can reloads the labels in Pie
            self._config.TAG_MODE.write(not self._config.TAG_MODE.read())
            if self._config.TAG_MODE.read():
                self._auto_combobox.set(self._manual_combobox.read())
                self._auto_combobox.save()
                # Reset hidden combobox to prevent unnecessary icon loading
                self._manual_combobox.set("---Select tag---")
                self._manual_combobox.save()
            else:
                self._manual_combobox.set(self._auto_combobox.read())
                self._manual_combobox.save()

        mode_button = SafeConfirmButton(confirm_text="Change?")
        mode_button.setFixedHeight(mode_button.sizeHint().height()*2)
        mode_button.clicked.connect(switch_mode)

        self._config.TAG_MODE.register_callback(self._set_tag_mode)
        return mode_button

    def _init_auto_combobox(self) -> StringComboBox:
        """Create tag mode combobox, which sets tag presets to the pie."""
        auto_combobox = StringComboBox(
            config_field=self._config.TAG_NAME,
            allowed_values=self._label_creator.fetch_groups())

        def set_order_of_previous_group(previous_group: str):
            # Save order of previous group
            values = self._order_handler.values
            self._group_order_holder.set_order(previous_group, values)

        def replace_labels():
            # Replace the labels with values from the updated group
            new_group = auto_combobox.read()
            labels = self._label_creator.labels_from_group(new_group)
            self._order_handler.replace_labels(labels)

        def on_new_tag() -> None:
            if self._config.TAG_NAME.read() != auto_combobox.read():
                set_order_of_previous_group(auto_combobox.read())
                auto_combobox.set(self._config.TAG_NAME.read())
                replace_labels()
        self._config.TAG_NAME.register_callback(on_new_tag)

        def on_text_change():
            if self._config.TAG_NAME.read() != auto_combobox.read():
                set_order_of_previous_group(self._config.TAG_NAME.read())
                self._config.TAG_NAME.write(auto_combobox.read())
                replace_labels()
        auto_combobox.widget.currentTextChanged.connect(on_text_change)

        return auto_combobox

    def _init_manual_combobox(self) -> StringComboBox:
        def display_group() -> None:
            """Update preset widgets according to tag selected in combobox."""
            picked_group = manual_combobox.read()
            labels = self._label_creator.labels_from_group(
                group=picked_group,
                sort=False)
            self._scroll_area.replace_handled_labels(labels)
            self._scroll_area.apply_search_bar_filter()
            manual_combobox.save()

        manual_combobox = StringComboBox(
            config_field=self._config.LAST_TAG_SELECTED,
            allowed_values=(
                ["---Select tag---", "All"]
                + self._label_creator.fetch_groups()))

        manual_combobox.widget.currentTextChanged.connect(display_group)
        display_group()

        return manual_combobox

    def _set_tag_mode(self) -> None:
        """Set the pie mode to tag (True) or manual (False)."""
        if self._config.TAG_MODE.read():
            # moving to tag mode
            self._mode_button.main_text = "Tag mode"
            self._mode_button.icon = Krita.get_icon("tag")
            self._scroll_area.hide()
            self._manual_combobox.widget.hide()
            self._auto_combobox.widget.show()

            labels = self._label_creator.labels_from_config(self._config)
            self._order_handler.replace_labels(labels)
        else:
            # moving to manual mode
            self._mode_button.main_text = "Manual mode"
            self._mode_button.icon = Krita.get_icon("color-to-alpha")
            self._scroll_area.show()
            self._manual_combobox.widget.show()
            self._auto_combobox.widget.hide()
