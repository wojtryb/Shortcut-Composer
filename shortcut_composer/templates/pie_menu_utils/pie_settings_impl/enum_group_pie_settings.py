# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from core_components import Controller
from api_krita.enums.helpers import EnumGroup
from templates.pie_menu_utils import PieSettings
from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from ..pie_style_holder import PieStyleHolder
from ..pie_label import PieLabel
from .common_utils import GroupManager, GroupScrollArea


class EnumGroupPieSettings(PieSettings):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        config: NonPresetPieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        super().__init__(config, style_holder)

        self._action_values = GroupScrollArea(
            fetcher=EnumGroupManager(controller),
            unscaled_label_style=self._style_holder.unscaled_label_style,
            columns=3,
            field=self._config.field("Last tag selected", "All"),
            additional_fields=["All"])
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._action_values.widgets_changed.connect(self._refresh_draggable)
        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie non draggable and disabled."""
        self._action_values.mark_used_values(self._config.values())


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
