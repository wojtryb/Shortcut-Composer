# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from enum import Enum

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from templates.pie_menu_utils import (
    Label,
    PieStyle,
    PieSettings,
    NonPresetPieConfig)
from .common_utils import GroupScrollArea, GroupManager


class EnumGroupPieSettings(PieSettings):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        config: NonPresetPieConfig,
        style: PieStyle,
        *args, **kwargs
    ) -> None:
        super().__init__(config, style)

        self._action_values = GroupScrollArea(
            fetcher=EnumGroupManager(controller),
            style=self._style,
            columns=3,
            field=self._config.field("Last tag selected", "All"),
            additional_fields=["All"])
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._action_values.widgets_changed.connect(self._refresh_draggable)
        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_values(self._config.values())


class EnumGroupManager(GroupManager):
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._enum_type = self._controller.TYPE

    def fetch_groups(self) -> List[str]:
        return list(self._enum_type._groups_.keys())

    def get_values(self, group: str) -> List[Enum]:
        if group == "All":
            return list(self._enum_type._member_map_.values())
        return self._enum_type._groups_[group]

    def create_labels(self, values: List[Enum]) -> List[Label[Enum]]:
        """Create labels from list of preset names."""
        labels = [Label.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]
