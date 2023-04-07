# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import (
    TypeVar,
    Generic,
    Optional,
    List)

from .api_krita import Krita
from .parsers import Parser
from .field_base import FieldBase

T = TypeVar('T')


class NonListField(FieldBase, Generic[T]):
    """Config field containing a basic, non-list value."""

    def __init__(
        self,
        config_group: str,
        name: str,
        default: T,
        parser_type: Optional[type] = None,
    ) -> None:
        super().__init__(config_group, name, default)
        self._parser: Parser[T] = self._get_parser(type(self.default))

    def read(self) -> T:
        """Return value from .kritarc parsed to field type."""
        raw = Krita.read_setting(self.config_group, self.name)
        if raw is None:
            return self.default
        return self._parser.parse_to(raw)

    def _to_string(self, value: T) -> str:
        """Parse the field value to string using parser."""
        return self._parser.parse_from(value)


class ListField(FieldBase, Generic[T]):
    """Config field containing a list value."""

    def __init__(
        self,
        config_group: str,
        name: str,
        default: List[T],
        parser_type: Optional[type] = None,
    ) -> None:
        super().__init__(config_group, name, default)
        self._parser: Parser[T] = self._get_parser(self._get_type(parser_type))

    def _get_type(self, passed_type: Optional[type]) -> type:
        """
        Determine parser type based on default value or passed type.

        - For non empty list, parser depends on first list element.
        - For empty list, parsed type must be used directly
        """
        if not self.default:
            if passed_type is None:
                raise ValueError("Type not given for a list")
            return passed_type
        return type(self.default[0])

    def read(self) -> List[T]:
        """
        Return value from .kritarc parsed to field type.

        Each list element requires parsing.
        """
        raw = Krita.read_setting(self.config_group, self.name)
        if raw is None:
            return self.default

        values_list = raw.split("\t")
        return [self._parser.parse_to(value) for value in values_list]

    def _to_string(self, value: List[T]) -> str:
        """Convert list of values to string by parsing each element alone."""
        return "\t".join([self._parser.parse_from(item) for item in value])
