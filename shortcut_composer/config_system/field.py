# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, Callable, List

T = TypeVar('T')


class Field(Generic[T]):

    def __new__(
        cls,
        config_group: str,
        name: str,
        default: T,
        passed_type: Optional[type] = None
    ) -> 'Field[T]':
        from .field_implementations import ListField, NonListField

        cls.original = super().__new__
        if isinstance(default, list):
            return ListField(config_group, name, default, passed_type)
        return NonListField(config_group, name, default, passed_type)

    name: str
    default: T

    def write(self, value: T) -> None: ...
    def read(self) -> T: ...
    def register_callback(self, callback: Callable[[], None]): ...
    def reset_default(self) -> None: ...


class FieldGroup:
    def __init__(self, name: str) -> None:
        self.name = name
        self._fields: List[Field] = []
        self._callbacks: List[Callable[[], None]] = []

    def __call__(
        self,
        name: str,
        default: T,
        passed_type: Optional[type] = None
    ) -> Field[T]:
        field = Field(self.name, name, default, passed_type)
        self._fields.append(field)
        for callback in self._callbacks:
            field.register_callback(callback)
        return field

    def reset_default(self):
        for field in self._fields:
            field.reset_default()

    def register_callback(self, callback: Callable[[], None]):
        self._callbacks.append(callback)
        for field in self._fields:
            field.register_callback(callback)

    def __iter__(self):
        return iter(self._fields)
