# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, Callable, final, List
from abc import ABC, abstractmethod
from enum import Enum

from api_krita import Krita
from .parsers import Parser, BoolParser, EnumParser, BasicParser
from .fields import Field

T = TypeVar('T')
E = TypeVar('E', bound=Enum)
ListT = TypeVar('ListT', bound=List[Enum])


class FieldBase(ABC, Field, Generic[T]):
    def __new__(cls, *args, **kwargs) -> 'FieldBase[T]':
        obj = object.__new__(cls)
        obj.__init__(*args, **kwargs)
        return obj

    def __init__(self, name: str, default: T, type: Optional[type] = None):
        self.name = name
        self.default = default
        self._type = self._get_type(type)
        self._parser = self._get_parser()
        self._on_change_callbacks: List[Callable[[], None]] = []

    @abstractmethod
    def _get_type(self, passed_type: Optional[type]) -> type: ...

    @abstractmethod
    def _to_string(self, value: T) -> str: ...

    @abstractmethod
    def read(self) -> T: ...

    @final
    def register_callback(self, callback: Callable[[], None]):
        self._on_change_callbacks.append(callback)

    def _get_parser(self) -> Parser[T]:
        if issubclass(self._type, Enum):
            return EnumParser(self._type)  # type: ignore

        return {
            int: BasicParser(int),
            float: BasicParser(float),
            str: BasicParser(str),
            bool: BoolParser()
        }[self._type]

    @final
    def write(self, value: T):
        if self._is_write_redundant(value):
            return

        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value=self._to_string(value))
        for callback in self._on_change_callbacks:
            callback()

    @final
    def _is_write_redundant(self, value: T):
        if self.read() == value:
            return True
        current_value = self._read_raw()
        return current_value is None and value == self.default

    @final
    def _read_raw(self) -> Optional[str]:
        red_value = Krita.read_setting(
            group="ShortcutComposer",
            name=self.name,
            default="Not stored")
        return None if red_value == "Not stored" else red_value

    @final
    def reset_default(self) -> None:
        self.write(self.default)
