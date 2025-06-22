# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from config_system import Field
from config_system.ui import StringComboBox
from composer_utils.label.complex_widgets import ScrollArea
from core_components import Controller
from ..pie_config import PieConfig
from ..group_manager import GroupManager
from ..group_manager_impl import dispatch_group_manager
from ..pie_style_holder import PieStyleHolder
from ..pie_widget_utils import OrderHandler


class ValuesListTab(QWidget):

    def __init__(
        self,
        config: PieConfig,
        order_handler: OrderHandler,
        controller: Controller,
        style_holder: PieStyleHolder,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._order_handler = order_handler
        self._style_holder = style_holder

        self._label_creator = dispatch_group_manager(controller)
        self._scroll_area = self._init_scroll_area()
        self._mode_button = self._init_mode_button()
        self._auto_combobox = self._init_auto_combobox()
        self._manual_combobox = self._init_manual_combobox()

        self._set_tag_mode(self._config.TAG_MODE.read())
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
            is_tag_mode = not self._config.TAG_MODE.read()
            self._set_tag_mode(is_tag_mode)
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
            lambda: self._set_tag_mode(self._config.TAG_MODE.read(), False))
        return mode_button

    def _init_auto_combobox(self) -> '_GroupComboBox':
        """Create tag mode combobox, which sets tag presets to the pie."""
        def handle_picked_tag() -> None:
            """Save used tag in config and report the values changed."""
            # Save order in previous tag
            self._order_handler.values
            self._config.set_values(self._order_handler.values)

            # Switch to new tag and replace labels with its values
            auto_combobox.save()
            picked_group = auto_combobox.read()
            labels = self._label_creator.labels_from_group(picked_group)
            self._order_handler.replace_labels(labels)

        auto_combobox = _GroupComboBox(
            last_value_field=self._config.TAG_NAME,
            group_manager=self._label_creator,
            pretty_name="Tag name")

        auto_combobox.widget.currentTextChanged.connect(handle_picked_tag)
        return auto_combobox

    def _init_manual_combobox(self) -> '_GroupComboBox':
        def _display_group() -> None:
            """Update preset widgets according to tag selected in combobox."""
            picked_group = manual_combobox.widget.currentText()
            labels = self._label_creator.labels_from_group(picked_group)
            self._scroll_area.replace_handled_labels(labels)
            self._scroll_area._apply_search_bar_filter()
            manual_combobox.save()

        manual_combobox = _GroupComboBox(
            last_value_field=self._config.LAST_TAG_SELECTED,
            group_manager=self._label_creator,
            additional_fields=["---Select tag---", "All"])

        manual_combobox.widget.currentTextChanged.connect(_display_group)
        _display_group()

        return manual_combobox

    def _set_tag_mode(self, value: bool, notify: bool = True) -> None:
        """Set the pie mode to tag (True) or manual (False)."""
        if notify:
            self._config.TAG_MODE.write(value)
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


class _GroupComboBox(StringComboBox):

    def __init__(
        self,
        last_value_field: Field[str],
        group_manager: GroupManager,
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        additional_fields: list[str] = [],
    ) -> None:
        self._additional_fields = additional_fields
        self._group_manager = group_manager
        super().__init__(last_value_field, parent, pretty_name)
        self.config_field.register_callback(
            lambda: self.set(self.config_field.read()))

    def reset(self) -> None:
        """Replace list of available tags with those red from database."""
        self._combo_box.clear()
        self._combo_box.addItems(self._additional_fields)
        self._combo_box.addItems(self._group_manager.fetch_groups())
        self.set(self.config_field.read())
