# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, Callable

T = TypeVar('T')


class Field(Generic[T]):

    def __new__(
        cls,
        name: str,
        default: T,
        passed_type: Optional[type] = None
    ) -> 'Field[T]':
        from .field_implementations import ListField, NonListField

        cls.original = super().__new__
        if isinstance(default, list):
            return ListField(name, default, passed_type)
        return NonListField(name, default, passed_type)

    name: str
    default: T

    def write(self, value: T) -> None: ...
    def read(self) -> T: ...
    def register_callback(self, callback: Callable[[], None]): ...
    def reset_default(self) -> None: ...
