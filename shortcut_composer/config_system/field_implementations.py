# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import (
    TypeVar,
    Generic,
    Optional,
    Type,
    List)
from enum import Enum

from .parsers import Parser
from .field_base import FieldBase

T = TypeVar('T')
E = TypeVar('E', bound=Enum)
ListT = TypeVar('ListT', bound=List[Enum])


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
