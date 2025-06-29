# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from ..pie_group_manager import PieGroupManager


class InvalidPieGroupManager(PieGroupManager):
    def __init__(self) -> None:
        pass

    def fetch_groups(self) -> list[str]:
        return []

    def values_from_group(self, group: str, sort: bool = True) -> list:
        return []
