# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Type, Protocol
from enum import Enum

from PyQt5.QtGui import QColor

T = TypeVar("T")
Basic = TypeVar("Basic", str, int, float)
EnumT = TypeVar("EnumT", bound=Enum)


def dispatch_parser(parser_type: type) -> 'Parser':
    """Return a proper field parser based on given type."""
    if issubclass(parser_type, Enum):
        return EnumParser(parser_type)

    return {
        int: BasicParser(int),
        float: BasicParser(float),
        str: BasicParser(str),
        bool: BoolParser(),
        QColor: ColorParser()
    }[parser_type]


class Parser(Generic[T], Protocol):
    """Parses from string to specific type and vice-versa."""

    type: type

    def parse_to(self, value: str) -> T:
        """Parse from string to specific type."""
        ...

    def parse_from(self, value: T) -> str:
        """Parse from specific type to string."""
        ...


class BasicParser(Parser[Basic]):
    """Parses from string to basic type and vice-versa."""

    def __init__(self, type: Type[Basic]) -> None:
        self.type = type

    def parse_to(self, value: str) -> Basic:
        """Parse from string to a string or number to ."""
        return self.type(value)

    def parse_from(self, value: Basic) -> str:
        """Parse from string to string or number."""
        return str(value)


class BoolParser(Parser[bool]):
    """Parses from string to bool and vice-versa."""

    type = bool

    def parse_to(self, value: str) -> bool:
        """Parses from string to bool."""
        if value not in ("true", "false"):
            raise ValueError(f"Cant parse {value} to bool")
        return value == "true"

    def parse_from(self, value: bool) -> str:
        """Parses from bool to string."""
        return str(value).lower()


class EnumParser(Parser[EnumT]):
    """Parses from string to enum and vice-versa."""

    def __init__(self, type: Type[EnumT]) -> None:
        self.type = type

    def parse_to(self, value: str) -> EnumT:
        """Parse from string to enum."""
        return self.type[value]  # type: ignore

    def parse_from(self, value: EnumT) -> str:
        """Parse from enum to string."""
        return str(value.name)


class ColorParser(Parser[QColor]):
    """Parses from string to QColor and vice-versa."""

    type = QColor

    def parse_to(self, value: str) -> QColor:
        """Parses from string to QColor."""
        element_list = value.split(",")
        return QColor(*map(int, element_list))

    def parse_from(self, value: QColor) -> str:
        """Parses from QColor to string."""
        return f"{value.red()},{value.green()},{value.blue()},{value.alpha()}"
