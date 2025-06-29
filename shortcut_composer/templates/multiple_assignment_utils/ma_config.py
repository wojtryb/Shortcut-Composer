# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar

from config_system import FieldGroup
from data_components import Tag

T = TypeVar("T")


class MaConfig(FieldGroup, Generic[T]):

    def __init__(
        self,
        name: str,
        value_type: type,
        values: list[T] | Tag,
        default_value: T,
    ) -> None:
        super().__init__(name)

        default_values = [] if isinstance(values, Tag) else values
        self.VALUES = self.field(
            name="Values",
            default=default_values,
            parser_type=value_type)
        """Values to cycle with short key presses."""

        self.DEFAULT_VALUE = self.field(
            name="Default value",
            default=default_value)
        """Value activated after a long press."""

        group_mode = isinstance(values, Tag)
        self.GROUP_MODE = self.field(
            name="Group mode",
            default=group_mode)
        """If true, the pie operates on groups, not individual values."""

        group_name = values.tag_name if isinstance(values, Tag) else ""
        self.GROUP_NAME = self.field(
            name="Group",
            default=group_name)
        """Name of selected group if in group mode."""

        self.LAST_GROUP_SELECTED = self.field(
            name="Last group selected",
            default="---Select group---")
        """Previously selected group in the ScrollArea in settings."""
