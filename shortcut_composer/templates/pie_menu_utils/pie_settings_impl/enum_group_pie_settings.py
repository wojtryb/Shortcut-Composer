# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from core_components import Controller
from api_krita.enums.helpers import EnumGroup
from composer_utils.label.complex_widgets import ScrollArea
from templates.pie_menu_utils import PieSettings
from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from ..pie_style_holder import PieStyleHolder
from ..pie_label import PieLabel
from .common_utils import GroupManager, GroupComboBox


class EnumGroupPieSettings(PieSettings):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        config: NonPresetPieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        super().__init__(controller, config, style_holder)

        self._scroll_area = self._init_scroll_area()
        self._manual_combobox = self._init_manual_combobox()

        self._tab_holder.insertTab(1, self._scroll_area, "Values")
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

    def _init_manual_combobox(self) -> GroupComboBox:
        manager = EnumGroupManager(self._controller)

        def _display_group() -> None:
            """Update preset widgets according to tag selected in combobox."""
            picked_group = manual_combobox.widget.currentText()
            values = manager.get_values(picked_group)
            self._scroll_area.replace_handled_labels(
                manager.create_labels(values))
            self._scroll_area._apply_search_bar_filter()
            manual_combobox.save()

        manual_combobox = GroupComboBox(
            last_value_field=self._config.field(
                "Last tag selected",
                "---Select tag---"),
            group_manager=manager,
            additional_fields=["---Select tag---", "All"])

        # Do not display combobox with groups, when there is only one group
        if len(manager.fetch_groups()) > 1:
            self._scroll_area._layout.insertWidget(0, manual_combobox.widget)

        manual_combobox.widget.currentTextChanged.connect(_display_group)
        _display_group()

        return manual_combobox


class EnumGroupManager(GroupManager):
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._enum_type = self._controller.TYPE

    def fetch_groups(self) -> list[str]:
        return list(self._enum_type._groups_.keys())

    def get_values(self, group: str) -> list[Enum]:
        if group == "All":
            return list(self._enum_type._member_map_.values())
        return self._enum_type._groups_[group]

    def create_labels(self, values: list[Enum]) -> list[PieLabel[Enum]]:
        """Create labels from list of preset names."""
        labels = [PieLabel.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]
