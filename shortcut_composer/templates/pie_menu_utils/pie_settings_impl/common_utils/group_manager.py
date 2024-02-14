# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Protocol
from enum import Enum

from composer_utils.label.label_interface import LabelInterface


class GroupManager(Protocol):
    def fetch_groups(self) -> list: ...
    def get_values(self, group: str) -> list: ...
    def create_labels(self, values: list[Enum]) -> list[LabelInterface]: ...
