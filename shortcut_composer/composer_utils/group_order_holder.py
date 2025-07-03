# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar
from config_system import Field

T = TypeVar("T")


class GroupOrderHolder(Generic[T]):
    """
    Allows to read and write value order in a group, stored in config.

    Shortcut Composer defines value groups. Presets are grouped with
    tags, actions and tools are divided into groups with EnumGroup.

    It also allows to specify and save custom order of those groups, by
    dragging values inside any PieWidget in a group mode.

    This class reads and writes order inside a group, saved between
    sessions in config. All objects share the config fields, that are
    created, when any object tries to access the order for the first
    time.
    """

    fields: dict[str, Field] = {}

    def __init__(self, value_type: type[T]) -> None:
        self._value_type = value_type

    def get_order(self, group_name: str) -> list[T]:
        """Return stored order of given group. [] if group not known."""
        typed_name = self._typed_name(group_name)
        if typed_name not in self.fields:
            self.fields[typed_name] = self._create_field(typed_name)
        return self.fields[typed_name].read()

    def set_order(self, group_name: str, values: list[T]) -> None:
        """Save order of given group."""
        typed_name = self._typed_name(group_name)
        if typed_name not in self.fields:
            self.fields[typed_name] = self._create_field(typed_name)
        self.fields[typed_name].write(values)

    def _typed_name(self, group_name: str):
        """Name used in config that include the value type."""
        return f"{self._value_type.__qualname__}_{group_name}"

    def _create_field(self, typed_name: str) -> Field[list[T]]:
        """Create config field for storing an order of single group."""
        return Field(
            config_group="ShortcutComposer: Group order",
            name=typed_name,
            default=[],
            parser_type=self._value_type)
