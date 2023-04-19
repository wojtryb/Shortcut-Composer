# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from api_krita.wrappers import Database


class Tag(List[str]):
    """List representing names of presets in a tag of given name."""

    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.refresh()

    def refresh(self):
        """Update itself with current list of presets that belong to tag."""
        self.clear()
        self.extend(self._read_presets())

    def _read_presets(self) -> List[str]:
        """Read the brush presets from the database using tag name."""
        with Database() as database:
            return database.get_preset_names_from_tag(self.tag_name)
