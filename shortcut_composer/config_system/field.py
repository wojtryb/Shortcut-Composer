# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable

T = TypeVar('T')


class Field(Generic[T]):
    """
    Representation of a single configuration value.

    Based on `local`, data can be saved in kritarc or .kra document.

    Once initialized with its group name, name, and default value, it
    allows to:
    - write a given value to kritarc or .kra.
    - read current value and parse it to correct python type.
    - reset the value to default.
    - register a callback run on each value change.

    Type of default value passed on initialization is remembered, and used
    to parse values both on read and write. Supported types are:
    - `int`, `list[int]`,
    - `float`, `list[float]`,
    - `str`, `list[str]`,
    - `bool`, `list[bool]`,
    - `Enum`, `list[Enum]`

    For empty, homogeneous lists, `parser_type` argument must be used to
    determine type of list elements.

    Default values are not saved when until the field does not exist in
    its location. Repeated saves of the same value are filtered, so that
    callbacks are not called when the same value is written multiple
    times one after the other.
    """

    def __new__(
        cls,
        config_group: str,
        name: str,
        default: T,
        parser_type: type | None = None,
        local: bool = False,
    ) -> 'Field[T]':
        from .field_base_impl import ListField, NonListField

        cls.original = super().__new__
        if not isinstance(default, list):
            return NonListField(
                config_group, name, default, parser_type, local)
        return ListField(config_group, name, default, parser_type, local)

    config_group: str
    """Configuration section in kritarc toml file."""
    name: str
    """Field name in entire config group."""
    default: T
    """Default value used when the field is not present in file."""

    def write(self, value: T) -> None:
        """Write a value to kritarc file."""

    def read(self) -> T:
        """Return value from kritarc parsed to field type."""
        ...

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register a method which will be called when field value changes."""

    def reset_default(self) -> None:
        """Write a default value to kritarc file."""
        ...
