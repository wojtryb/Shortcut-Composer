# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Type, Protocol
from enum import Enum

T = TypeVar("T")
Basic = TypeVar("Basic", str, int, float)
EnumT = TypeVar("EnumT", bound=Enum)


class Parser(Generic[T], Protocol):
    def parse_to(self, value: str) -> T:
        ...

    def parse_from(self, value: T) -> str:
        ...


class BasicParser(Parser[Basic]):
    def __init__(self, type: Type[Basic]) -> None:
        self.type = type

    def parse_to(self, value: str) -> Basic:
        return self.type(value)

    def parse_from(self, value: Basic) -> str:
        return str(value)


class BoolParser(Parser[bool]):
    def parse_to(self, value: str) -> bool:
        if value not in ("true", "false"):
            raise ValueError(f"Cant parse {value} to bool")
        return value == "true"

    def parse_from(self, value: bool) -> str:
        return str(value).lower()


class EnumParser(Parser[EnumT]):
    def __init__(self, type: Type[EnumT]) -> None:
        self.type = type

    def parse_to(self, value: str) -> EnumT:
        return self.type[value]

    def parse_from(self, value: EnumT) -> str:
        return str(value.name)
