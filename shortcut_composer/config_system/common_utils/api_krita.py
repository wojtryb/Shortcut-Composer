# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Required part of api_krita package, so that no dependency is needed."""

from typing import Any, Protocol
from dataclasses import dataclass

from krita import Krita as Api
from PyQt5.QtCore import QByteArray


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    def __init__(self) -> None:
        self.instance = Api.instance()

    def read_setting(
        self,
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> str | None:
        """
        Read a setting from kritarc file.

        - Return string red from file if present
        - Return default if it was given
        - Return None if default was not given
        """
        red_value = self.instance.readSetting(group, name, default)
        return None if red_value == "Not stored" else red_value

    def write_setting(self, group: str, name: str, value: Any) -> None:
        """Write setting to kritarc file. Value type will be lost."""
        self.instance.writeSetting(group, name, str(value))

    def get_active_document(self) -> 'Document | None':
        """Return wrapper of krita `Document`."""
        document = self.instance.activeDocument()
        if document is None:
            return None
        return Document(document)


class KritaDocument(Protocol):
    """Krita `Document` object API."""

    def setAnnotation(
        self,
        type: str,
        description: str,
        annotation: bytes) -> None: ...

    def annotation(self, type: str) -> QByteArray: ...
    def annotationTypes(self) -> list[str]: ...


@dataclass
class Document:
    """Wraps krita `Document` for typing, docs and PEP8 compatibility."""

    document: KritaDocument

    def read_annotation(self, name: str) -> str:
        """Read annotation from .kra document parsed as string."""
        return self.document.annotation(name).data().decode(encoding="utf-8")

    def write_annotation(self, name: str, description: str, value: str):
        """Write annotation to .kra document."""
        self.document.setAnnotation(
            name,
            description,
            value.encode(encoding="utf-8"))

    def contains_annotation(self, name: str) -> bool:
        """Return if annotation of given name is stored in .kra."""
        return name in self.document.annotationTypes()


Krita = KritaInstance()
