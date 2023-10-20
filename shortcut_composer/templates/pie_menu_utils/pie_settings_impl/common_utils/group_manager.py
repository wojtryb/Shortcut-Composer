# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Protocol
from enum import Enum

from ...pie_label import PieLabel


class GroupManager(Protocol):
    def fetch_groups(self) -> list: ...
    def get_values(self, group: str) -> list: ...
    def create_labels(self, values: List[Enum]) -> List[PieLabel]: ...
