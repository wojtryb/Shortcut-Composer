# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NoReturn

from ..pie_group_manager import PieGroupManager


class InvalidPieGroupManager(PieGroupManager):
    def __init__(self, unsupported_type: type) -> None:
        self._message = f"Cannot create groups with type {unsupported_type}"

    def fetch_groups(self) -> NoReturn:
        raise NotImplementedError(self._message)

    def values_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> NoReturn:
        raise NotImplementedError(self._message)
