# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_label import PieLabel
from .group_manager import GroupManager


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
        return self._enum_type._groups_[group]

    def create_labels(
        self,
        values: list[EnumGroup]
    ) -> list[PieLabel[EnumGroup]]:
        """Create labels from list of preset names."""
        labels = [PieLabel.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]
