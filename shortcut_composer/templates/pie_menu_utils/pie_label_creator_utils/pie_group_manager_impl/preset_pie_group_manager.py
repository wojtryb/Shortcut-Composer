# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.wrappers import Database
from composer_utils import GroupOrderHolder
from ..pie_group_manager import PieGroupManager


class PresetPieGroupManager(PieGroupManager[str]):
    """Reads preset names that belong to a group (krita tag)."""

    def __init__(self) -> None:
        self._group_order_holder = GroupOrderHolder(str)

    def fetch_groups(self) -> list[str]:
        """Return list of tags red from krita database."""
        with Database() as database:
            return database.get_brush_tags()

    def values_from_group(self, group: str, sort: bool = True) -> list[str]:
        """
        Return all preset names that belong to given tag.

        If `sort` is True, order from GroupOrderHolder is used.
        Otherwise they will come in the initial order from database.

        When tag is unknown, empty list is returned.

        Use tag 'All' to get all krita presets.
        """
        if group == "All":
            return list(Krita.get_presets().keys())

        with Database() as database:
            from_krita = database.get_preset_names_from_tag(group)
        if not sort:
            return from_krita
        from_config = self._group_order_holder.get_order(group)

        preset_order = [p for p in from_config if p in from_krita]
        missing = [p for p in from_krita if p not in from_config]

        return preset_order + missing
