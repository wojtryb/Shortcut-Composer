# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from config_system import Field
from ..pie_label import PieLabel
from ..group_manager import GroupManager


class EnumGroupManager(GroupManager):
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._enum_type = self._controller.TYPE

    def fetch_groups(self) -> list[str]:
        return list(self._enum_type._groups_.keys())

    def get_values(self, group: str) -> list[EnumGroup]:
        if group == "All":
            return list(self._enum_type._member_map_.values())
        elif group not in self._enum_type._groups_:
            return []

        from_krita = self._enum_type._groups_[group]

        field = Field(
            config_group="ShortcutComposer: Tag order",
            name=group,
            default=[],
            parser_type=self._controller.TYPE)
        from_config = field.read()

        known_order = [v for v in from_config if v in from_krita]
        missing = [v for v in from_krita if v not in from_config]

        return known_order + missing

    def create_labels(
        self,
        values: list[EnumGroup]
    ) -> list[PieLabel[EnumGroup]]:
        """Create labels from list of preset names."""
        labels = [PieLabel.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]
