# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.wrappers import Database
from composer_utils import GroupOrderHolder


class Tag(list[str]):
    """List representing names of presets in a tag of given name."""

    def __init__(self, tag_name: str) -> None:
        self.tag_name = tag_name
        self._group_order_holder = GroupOrderHolder(str)
        self.refresh()

    def refresh(self) -> None:
        """Update itself with current list of presets that belong to tag."""
        self.clear()
        self.extend(self._read_presets())

    def _read_presets(self) -> list[str]:
        """
        Read the brush presets from the database using tag name.

        Take into consideration order stored in config.
        """
        with Database() as database:
            from_krita = database.get_preset_names_from_tag(self.tag_name)

        from_config = self._group_order_holder.get_order(self.tag_name)

        preset_order = [p for p in from_config if p in from_krita]
        missing = [p for p in from_krita if p not in from_config]
        return preset_order + missing
