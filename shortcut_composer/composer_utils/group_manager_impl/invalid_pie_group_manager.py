# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from ..group_manager import GroupManager


class InvalidGroupManager(GroupManager):
    """GroupManager for types that have no defined groups."""

    def __init__(self) -> None:
        pass

    def fetch_groups(self) -> list[str]:
        """Return empty list."""
        return []

    def values_from_group(self, group: str, sort: bool = True) -> list:
        """Return empty list."""
        return []
