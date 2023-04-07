# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Optional, Callable, List
from .field import Field

T = TypeVar('T')


class FieldGroup:
    """
    Representation of section in .kritarc toml file.

    All fields in the group should be created using `field()` method.
    It simplifies the field creation by auto-completing the group name.

    FieldGroup holds and aggregates fields created with it.

    Allows to reset all the fields at once, as well as register a
    callback to all existing fields, as well as those that will be
    added to the group in the future.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._fields: List[Field] = []
        self._callbacks: List[Callable[[], None]] = []

    def field(
        self,
        name: str,
        default: T,
        passed_type: Optional[type] = None
    ) -> Field[T]:
        """Create and return a new field in the group."""
        field = Field(self.name, name, default, passed_type)
        self._fields.append(field)
        for callback in self._callbacks:
            field.register_callback(callback)
        return field

    def reset_default(self):
        """Reset values of all fields stored in this group."""
        for field in self._fields:
            field.reset_default()

    def register_callback(self, callback: Callable[[], None]):
        """Register a callback on every past and future field in group."""
        self._callbacks.append(callback)
        for field in self._fields:
            field.register_callback(callback)

    def __iter__(self):
        """Iterate over all fields in the group."""
        return iter(self._fields)
