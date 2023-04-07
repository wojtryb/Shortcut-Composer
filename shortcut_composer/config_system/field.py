# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, Callable, List

T = TypeVar('T')


class Field(Generic[T]):
    """
    Representation of a single value in .kritarc file.

    Fields are type aware, and allow to read and write from krita config
    automatically parsing to the value type.

    Type is determined based on default value passed on initialization.
    For empty, homogeneous lists, `parser_type` must be used to
    determine type of list elements.
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
        return NonListField(config_group, name, default, parser_type)

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


class FieldGroup:
    """
    Representation of section in .kritarc toml file.

    All fields in the group must be created using `field()` method.
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
