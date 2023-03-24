# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, List, Callable, final
from abc import ABC, abstractmethod
from enum import Enum

from api_krita import Krita
from .parsers import Parser, BoolParser, EnumParser, BasicParser

T = TypeVar('T')
ListT = TypeVar('ListT', bound=List[Enum])


def field(name: str, default: T, passed_type: Optional[type] = None
          ) -> 'FieldBase[T]':
    if isinstance(default, list):
        return ListField(name, default, passed_type)
    return NonListField(name, default, passed_type)


class FieldBase(Generic[T], ABC):
    def __init__(self, name: str, default: T, type: Optional[type] = None):
        self.name = name
        self.default = default
        self.type = self._get_type(type)
        self.parser = self._get_parser()
        self._on_change_callbacks: List[Callable[[], None]] = []

    def _get_type(self, passed_type: Optional[type]) -> type:
        if not isinstance(self.default, list):
            return type(self.default)
        if not self.default:
            if passed_type is None:
                raise ValueError("Type not given for a list")
            return passed_type
        return type(self.default[0])

    def _get_parser(self) -> Parser[T]:
        if issubclass(self.type, Enum):
            return EnumParser(self.type)  # type: ignore

        return {
            int: BasicParser(int),
            float: BasicParser(float),
            str: BasicParser(str),
            bool: BoolParser()
        }[self.type]  # type: ignore

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

    @abstractmethod
    def read(self) -> T: ...

    @final
    def reset_default(self) -> None:
        self.write(self.default)

    @final
    def register_callback(self, callback: Callable[[], None]):
        self._on_change_callbacks.append(callback)

    @final
    def _read_raw(self) -> Optional[str]:
        red_value = Krita.read_setting(
            group="ShortcutComposer",
            name=self.name,
            default="Not stored")
        return None if red_value == "Not stored" else red_value

    @final
    def _is_write_redundant(self, value: T):
        if self.read() == value:
            return True
        current_value = self._read_raw()
        return current_value is None and value == self.default

    @abstractmethod
    def _to_string(self, value: T) -> str: ...


class NonListField(FieldBase, Generic[T]):
    def read(self) -> T:
        raw = self._read_raw()
        if raw is None:
            return self.default
        return self.parser.parse_to(raw)

    def _to_string(self, value: T) -> str:
        return self.parser.parse_from(value)


class ListField(FieldBase, Generic[ListT]):
    def read(self) -> ListT:
        raw = self._read_raw()

        if raw is None:
            return self.default

        values_list = raw.split("\t")

        return [self.parser.parse_to(value) for value in values_list
                ]  # type: ignore

    def _to_string(self, value: ListT) -> str:
        return "\t".join([self.parser.parse_from(item) for item in value])
