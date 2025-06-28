# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, Generic, TypeVar

T = TypeVar("T")


class PieGroupManager(Protocol, Generic[T]):
    def fetch_groups(self) -> list[str]: ...

    def values_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[T]: ...
