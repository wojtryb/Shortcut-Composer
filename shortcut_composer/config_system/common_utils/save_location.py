# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Protocol
from enum import Enum

from .api_krita import Krita


class SupportsReadWrite(Protocol):
    """Allows reading and writing configuration which groups its fields."""

    def write(self, group: str, name: str, value: Any) -> None: ...
    def read(self, group: str, name: str, default: str) -> str | None: ...


class GlobalSettings(SupportsReadWrite):
    """Gives read/write interface for kritarc file."""

    @staticmethod
    def write(group: str, name: str, value: Any) -> None:
        """Write value to kritarc."""
        Krita.write_setting(group=group, name=name, value=value)

    @staticmethod
    def read(
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> str | None:
        """Write value from kritarc."""
        return Krita.read_setting(group=group, name=name, default=default)


class LocalSettings(SupportsReadWrite):
    """Gives read/write interface to .kra document annotations. """

    @staticmethod
    def write(group: str, name: str, value: Any) -> None:
        """Write value to .kra document as its annotation."""
        document = Krita.get_active_document()
        if document is not None:
            document.write_annotation(f"{group} {name}", "",  str(value))

    @staticmethod
    def read(
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> str | None:
        """Read value from .kra document stored in its annotation."""
        document = Krita.get_active_document()
        annotation_name = f"{group} {name}"

        if (document is None
                or not document.contains_annotation(annotation_name)):
            return None if default == "Not stored" else default

        return document.read_annotation(annotation_name)


class SaveLocation(Enum):
    """Enum with types of configuration fields. Grants the same interface."""

    GLOBAL = GlobalSettings
    LOCAL = LocalSettings

    def write(self, group: str, name: str, value: Any) -> None:
        """Write value to picked location."""
        self.value.write(group, name, value)

    def read(
        self,
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> str | None:
        """Read value from picked location."""
        return self.value.read(group, name, default)

    @property
    def value(self) -> SupportsReadWrite:
        """Enum holds values of type which support ReadWrite interface."""
        return super().value
