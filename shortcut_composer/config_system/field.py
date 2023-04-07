# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, Callable

T = TypeVar('T')


class Field(Generic[T]):
    """
    Representation of a single value in .kritarc file.

    Fields are type aware, and allow to read and write from krita config
    automatically parsing to the value type.

    Type of default value passed on initlization is remembered, and used
    to parse values both on read and write. Supported types are:
    -`int`,
    -`float`,
    -`str`,
    -`bool`,
    -`custom Enums`
    and homogeneous lists of every type above.

    For empty, homogeneous lists, `parser_type` must be used to
    determine type of list elements.

    Callbacks can be registered to the field, to run a method each time
    the value changes. Repeated saves of the same value are filtered.
    """

    def __new__(
        cls,
        config_group: str,
        name: str,
        default: T,
        parser_type: Optional[type] = None
    ) -> 'Field[T]':
        from .field_implementations import ListField, NonListField

        cls.original = super().__new__
        if isinstance(default, list):
            return ListField(config_group, name, default, parser_type)
        return NonListField(config_group, name, default)

    config_group: str
    """Configuration section in .kritarc toml file."""
    name: str
    """Field name in entire config group."""
    default: T
    """Default value used when the field is not present in file."""

    def write(self, value: T) -> None:
        """Write a value to .kritarc file."""

    def read(self) -> T:
        """Return value from .kritarc parsed to field type."""
        ...

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register a method which will be called when field value changes."""

    def reset_default(self) -> None:
        """Write a default value to .kritarc file."""
        ...
