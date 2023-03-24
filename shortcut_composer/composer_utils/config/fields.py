# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Optional, List, Type
from abc import ABC, abstractmethod
from enum import Enum

from api_krita import Krita

T = TypeVar('T')


class FieldBase(Generic[T], ABC):
    def __init__(self, name: str, default: T) -> None:
        self.name = name
        self.default = default

    def _read_raw(self) -> Optional[str]:
        red_value = Krita.read_setting(
            group="ShortcutComposer",
            name=self.name,
            default="Not stored")
        return None if red_value == "Not stored" else red_value

    def reset_default(self) -> None:
        self.write(self.default)

    def _is_write_redundant(self, value: T):
        current_value = self._read_raw()
        return current_value is None and value == self.default

    @abstractmethod
    def read(self) -> T: ...

    @abstractmethod
    def write(self, value: T): ...

    @property
    def type(self) -> Type[T]: ...


class ImmutableField(FieldBase, Generic[T]):
    "For str, int, float."

    def __init__(self, name: str, default: T) -> None:
        super().__init__(name, default)

    def read(self) -> T:
        raw = self._read_raw()
        if raw is None:
            return self.default
        return self.type(raw)

    def write(self, value: T) -> None:
        if self._is_write_redundant(value):
            return

        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value=value)

    @property
    def type(self):
        return type(self.default)


class EnumsListField(FieldBase):
    def read(self) -> List[Enum]:
        raw = self._read_raw()

        if raw is None:
            return self.default

        values_list = raw.split("\t")
        return [self.type[value] for value in values_list]

    def write(self, value: List[Enum]) -> None:
        if self._is_write_redundant(value):
            return

        to_write = "\t".join([enum.name for enum in value])
        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value=to_write)

    @property
    def type(self):
        element = self.default[0]
        return type(element)


class ImmutablesListField(FieldBase, Generic[T]):
    def __init__(self, name: str, default: List[T]) -> None:
        super().__init__(name, default)

    def read(self) -> List[T]:
        raw = self._read_raw()
        if raw is None:
            return self.default
        return [self.type(item) for item in raw.split("\t")]

    def write(self, value: List[T]) -> None:
        if self._is_write_redundant(value):
            return

        Krita.write_setting(
            group="ShortcutComposer",
            name=self.name,
            value="\t".join(map(str, value)))

    @property
    def type(self):
        return type(self.default[0])
