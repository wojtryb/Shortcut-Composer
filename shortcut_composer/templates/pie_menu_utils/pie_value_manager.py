# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol, Iterable

from .pie_config import PieConfig
from .pie_label import PieLabel


class PieValueManager(Protocol):
    def fetch_groups(self) -> list[str]: ...

    def labels_from_values(self, values: Iterable) -> list[PieLabel]: ...

    def labels_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[PieLabel]: ...

    def labels_from_config(self, config: PieConfig) -> list[PieLabel]: ...
