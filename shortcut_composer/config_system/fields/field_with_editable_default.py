# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from ..field import Field

from typing import Callable, Generic, TypeVar

T = TypeVar("T")
F = TypeVar("F", bound=Field)


class FieldWithEditableDefault(Field, Generic[T, F]):
    def __new__(cls, *args, **kwargs) -> 'FieldWithEditableDefault[T, F]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(self, field: F, field_with_default: Field[T]):
        self.field = field
        self._default_field = field_with_default

        def handle_change_of_default():
            self.field.default = self._default_field.read()
        self._default_field.register_callback(handle_change_of_default)
        handle_change_of_default()

        self.config_group = self.field.config_group
        self.name = self.field.name

    @property
    def default(self) -> T:
        return self.field.default

    @default.setter
    def default(self, value: T) -> None:
        self._default_field.write(value)

    def write(self, value: T) -> None:
        self.field.write(value)

    def read(self) -> T:
        return self.field.read()

    def register_callback(self, callback: Callable[[], None]) -> None:
        self.field.register_callback(callback)

    def reset_default(self) -> None:
        self.field.reset_default()
