# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, List, Callable, final, Protocol, Type
from abc import ABC, abstractmethod
from enum import Enum

from api_krita import Krita
from .parsers import Parser, BoolParser, EnumParser, BasicParser

T = TypeVar('T')
E = TypeVar('E', bound=Enum)
ListT = TypeVar('ListT', bound=List[Enum])


def field(name: str, default: T, passed_type: Optional[type] = None
          ) -> 'Field[T]':
    if isinstance(default, list):
        return ListField(name, default, passed_type)
    return NonListField(name, default, passed_type)


class Field(Generic[T], Protocol):

    name: str
    default: T

    def write(self, value: T) -> None: ...
    def read(self) -> T: ...
    def register_callback(self, callback: Callable[[], None]): ...

    @final
    def reset_default(self) -> None:
        self.write(self.default)


class FieldBase(Field, ABC, Generic[T]):
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


class NonListField(FieldBase, Generic[T]):

    _parser: Parser[T]

    def _get_type(self, passed_type: Optional[type]) -> Type[T]:
        return type(self.default)

    def read(self) -> T:
        raw = self._read_raw()
        if raw is None:
            return self.default
        return self._parser.parse_to(raw)

    def _to_string(self, value: T) -> str:
        return self._parser.parse_from(value)


class ListField(FieldBase, Generic[E]):

    _parser: Parser[E]

    def _get_type(self, passed_type: Optional[type]) -> type:
        if not self.default:
            if passed_type is None:
                raise ValueError("Type not given for a list")
            return passed_type
        return type(self.default[0])

    def read(self) -> List[E]:
        raw = self._read_raw()
        if raw is None:
            return self.default

        values_list = raw.split("\t")
        return [self._parser.parse_to(value) for value in values_list]

    def _to_string(self, value: List[E]) -> str:
        return "\t".join([self._parser.parse_from(item) for item in value])
