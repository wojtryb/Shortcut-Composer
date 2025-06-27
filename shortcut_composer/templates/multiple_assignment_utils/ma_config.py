# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar

from config_system import FieldGroup

T = TypeVar("T")


class MaConfig(FieldGroup, Generic[T]):

    def __init__(
        self,
        name: str,
        values: list[T],
        default_value: T,
    ) -> None:
        super().__init__(name)

        self.VALUES = self.field(
            name="Values",
            default=values)
        """Values to cycle with short key presses."""

        self.DEFAULT_VALUE = self.field(
            name="Default value",
            default=default_value)
        """Value activated after a long press."""

        self.LAST_GROUP_SELECTED = self.field(
            name="Last group selected",
            default="---Select group---")
        """Previously selected group in the ScrollArea in settings."""
