# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, Generic, TypeVar

from ..field import Field
from ..field_group import FieldGroup

T = TypeVar("T")
F = TypeVar("F", bound=Field)


class DualField(Field, Generic[T]):
    """
    Field switching save location based on passed field.

    Implementation uses two identical fields, but with different save
    location. Each time DualField is red or written, correct field is
    picked from the determiner field.

    NOTE: Callbacks are always stored in the global field, as they
    wouldn't run in local one when switching between documents.
    """
    def __new__(cls, *args, **kwargs) -> 'DualField[T]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(
        self,
        group: FieldGroup,
        is_local_determiner: Field[bool],
        field_name: str,
        default: T,
        parser_type: type | None = None
    ) -> None:
        self.name = field_name
        self.config_group = group.name
        self._is_local_determiner = is_local_determiner
        self._is_local_determiner.register_callback(self.refresh)
        self._loc = group.field(field_name, default, parser_type, local=True)
        self._glob = group.field(field_name, default, parser_type, local=False)

    @property
    def default(self) -> T:
        return self._glob.default

    @default.setter
    def default(self, value: T) -> None:
        self._loc.default = value
        self._glob.default = value

    def write(self, value: T) -> None:
        """
        Write to correct internal fields, based on determiner.
        Global field must always be written to activate callbacks.
        """
        if self._is_local_determiner.read():
            self._loc.write(value)
        self._glob.write(value)

    def read(self) -> T:
        """Read from local or global field, based on determiner."""
        if self._is_local_determiner.read():
            return self._loc.read()
        return self._glob.read()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Subscribe callback to both fields, as only one changes on write."""
        self._glob.register_callback(callback)

    def reset_default(self) -> None:
        """Reset both fields to default."""
        self._loc.reset_default()
        self._glob.reset_default()

    def refresh(self) -> None:
        """
        Write red value back to itself.
        Need to be performed manually when active document changes, as it does
        not run callbacks.
        """
        self.write(self.read())
