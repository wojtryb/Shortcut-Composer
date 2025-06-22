# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar
from config_system import Field

T = TypeVar("T")


class GroupOrderHolder(Generic[T]):

    fields: dict[str, Field] = {}

    def __init__(self, value_type: type[T]) -> None:
        self._value_type = value_type

    def get_order(self, group_name: str) -> list[T]:
        typed_name = self._typed_name(group_name)
        if typed_name not in self.fields:
            self.fields[typed_name] = self._create_field(typed_name)
        return self.fields[typed_name].read()

    def set_order(self, group_name: str, values: list[T]) -> None:
        typed_name = self._typed_name(group_name)
        if typed_name not in self.fields:
            self.fields[typed_name] = self._create_field(typed_name)
        self.fields[typed_name].write(values)

    def _typed_name(self, group_name: str):
        return f"{self._value_type.__qualname__}_{group_name}"

    def _create_field(self, typed_name: str) -> Field[list[T]]:
        return Field(
            config_group="ShortcutComposer: Group order",
            name=typed_name,
            default=[],
            parser_type=self._value_type)
