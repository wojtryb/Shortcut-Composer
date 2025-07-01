# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from composer_utils import GroupOrderHolder
from ..pie_group_manager import PieGroupManager


class EnumPieGroupManager(PieGroupManager[EnumGroup]):
    def __init__(self, enum_group_type: type[EnumGroup]) -> None:
        self._enum_group_type = enum_group_type
        self._group_order_holder = GroupOrderHolder(self._enum_group_type)

    def fetch_groups(self) -> list[str]:
        return list(self._enum_group_type._groups_.keys())

    def values_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[Enum]:
        if group == "All":
            return list(self._enum_group_type._member_map_.values())
        elif group not in self._enum_group_type._groups_:
            return []

        from_krita = self._enum_group_type._groups_[group]
        if not sort:
            return from_krita
        from_config = self._group_order_holder.get_order(group)

        known_order = [v for v in from_config if v in from_krita]
        missing = [v for v in from_krita if v not in from_config]

        return known_order + missing
