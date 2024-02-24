# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Callable, Iterator

from .field import Field

T = TypeVar('T')


class FieldGroup:
    """
    Representation of section in fields in kritarc file.

    All fields in the group should be created using `field()` method.
    It simplifies the field creation by auto-completing the group name.

    FieldGroup holds and aggregates fields created with it.

    Allows to reset all the fields at once, and register a callback to
    all its fields: both existing and future ones.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self._fields: list[Field] = []
        self._callbacks: list[Callable[[], None]] = []

    def field(
        self,
        name: str,
        default: T,
        parser_type: type | None = None,
        local: bool = False,
    ) -> Field[T]:
        """Create and return a new field in the group."""
        field = Field(self.name, name, default, parser_type, local)
        self._fields.append(field)
        for callback in self._callbacks:
            field.register_callback(callback)
        return field

    def reset_default(self) -> None:
        """Reset values of all fields stored in this group."""
        for field in self._fields:
            field.reset_default()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register a callback on every past and future field in group."""
        self._callbacks.append(callback)
        for field in self._fields:
            field.register_callback(callback)

    def __iter__(self) -> Iterator[Field]:
        """Iterate over all fields in the group."""
        return iter(self._fields)
