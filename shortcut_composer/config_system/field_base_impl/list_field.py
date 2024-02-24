# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from ..field_base import FieldBase
from .common_utils import dispatch_parser

T = TypeVar('T')


class ListField(FieldBase, Generic[T]):
    """Config field containing a list value."""

    def __init__(
        self,
        config_group: str,
        name: str,
        default: list[T],
        parser_type: type | None = None,
        local: bool = False,
    ) -> None:
        super().__init__(config_group, name, default, parser_type, local)
        self._parser = dispatch_parser(self._get_type(self.parser_type))

    def write(self, value: list[T]) -> None:
        for element in value:
            if not isinstance(element, self._parser.type):
                raise ValueError(f"{value} not of type {type(self.default)}")
        super().write(value)

    def _get_type(self, passed_type: type | None) -> type:
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

    def read(self) -> list[T]:
        """
        Return value from kritarc parsed to field type.

        Each list element requires parsing.
        """
        raw = self.location.read(self.config_group, self.name)
        if raw is None:
            return self.default

        if raw == "":
            return []

        values_list = raw.split("\t")
        return [self._parser.parse_to(value) for value in values_list]

    def _to_string(self, value: list[T]) -> str:
        """Convert list of values to string by parsing each element alone."""
        return "\t".join([self._parser.parse_from(item) for item in value])
