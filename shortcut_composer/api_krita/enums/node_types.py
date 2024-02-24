# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from krita import Krita as Api
from PyQt5.QtGui import QIcon


class NodeType(Enum):
    """
    Contains all known node types in krita.

    Example usage: `NodeType.PAINT_LAYER`
    """

    PAINT_LAYER = "paintlayer"
    GROUP_LAYER = "grouplayer"
    FILE_LAYER = "filelayer"
    FILTER_LAYER = "filterlayer"
    FILL_LAYER = "filllayer"
    CLONE_LAYER = "clonelayer"
    VECTOR_LAYER = "vectorlayer"
    TRANSPARENCY_MASK = "transparencymask"
    FILTER_MASK = "filtermask"
    TRANSFORM_MASK = "transformmask"
    SELECTION_MASK = "selectionmask"
    COLORIZE_MASK = "colorizemask"

    @property
    def icon(self) -> QIcon:
        """Return the icon of this node type."""
        return Api.instance().icon(self.value)

    @property
    def pretty_name(self) -> str:
        """Format node type name like: `Paint layer`."""
        return f"{self.name.replace('_', ' ').capitalize()}"
