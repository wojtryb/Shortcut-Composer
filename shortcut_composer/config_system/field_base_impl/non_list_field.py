# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from ..field_base import FieldBase
from .common_utils import dispatch_parser

T = TypeVar('T')


class NonListField(FieldBase, Generic[T]):
    """Config field containing a basic, non-list value."""

    def __init__(
        self,
        config_group: str,
        name: str,
        default: T,
        parser_type: type | None = None,
        local: bool = False,
    ) -> None:
        super().__init__(config_group, name, default, parser_type, local)
        self._parser = dispatch_parser(type(self.default))

    def read(self) -> T:
        """Return value from kritarc parsed to field type."""
        raw = self.location.read(self.config_group, self.name)
        if raw is None:
            return self.default
        return self._parser.parse_to(raw)

    def _to_string(self, value: T) -> str:
        """Parse the field value to string using parser."""
        return self._parser.parse_from(value)
