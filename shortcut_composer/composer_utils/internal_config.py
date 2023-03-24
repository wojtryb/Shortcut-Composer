# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, List
from enum import Enum

from api_krita import Krita

T = TypeVar('T')


class ConfigBase(Generic[T]):
    def __init__(self, name: str, default: T) -> None:
        self.name = name
        self.default = default

    def _read_raw(self) -> str:
        return Krita.read_setting(
            group="ShortcutComposer",
            name=self.name,
            default="",)

    def reset_default(self) -> None:
        self.write(self.default)

    def read(self) -> T: ...
    def write(self, value: T): ...


class BuiltinConfig(ConfigBase, Generic[T]):
    "For str, int and float"

    def __init__(self, name: str, default: T) -> None:
        super().__init__(name, default)

    def read(self) -> T:
        raw = self._read_raw()

        if raw == "":
            return self.default

        return type(self.default)(raw)

    def write(self, value: T) -> None:
        """Write given value to krita config file."""
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value=value)


class EnumListConfig(ConfigBase):
    def read(self) -> List[Enum]:
        raw = self._read_raw()

        if raw == "":
            return self.default

        element = self.default[0]
        values_list = raw.split("\t")

        enum_type = type(element)
        return [enum_type[value] for value in values_list]

    def write(self, value: List[Enum]) -> None:
        """Write given value to krita config file."""
        to_write = "\t".join([enum.name for enum in value])

        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value=to_write)


class BuiltinListConfig(ConfigBase):
    def __init__(self, name: str, default: List[T]) -> None:
        super().__init__(name, default)

    def read(self) -> List[T]:
        raw = self._read_raw()

        if raw == "":
            return self.default

        parse_type = type(self.default)
        return [parse_type(item) for item in raw.split("\t")]

    def write(self, value: List[T]) -> None:
        """Write given value to krita config file."""
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value="\t".join(map(str, value)))
