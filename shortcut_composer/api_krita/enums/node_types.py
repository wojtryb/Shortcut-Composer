# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from enum import Enum

from PyQt5.QtGui import QIcon

class NodeType(Enum):
    """
    Contains all known node types in krita.

    Example usage: `NodeType.PAINT_LAYER`

    Available node types:
    - `PAINT_LAYER`
    - `GROUP_LAYER`
    - `FILE_LAYER`
    - `FILTER_LAYER`
    - `FILL_LAYER`
    - `CLONE_LAYER`
    - `VECTOR_LAYER`
    - `TRANSPARENCY_MASK`
    - `FILTER_MASK`
    - `TRANSFORM_MASK`
    - `SELECTION_MASK`
    - `COLORIZE_MASK`
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
        icon_name = _ICON_NAME_MAP.get(self, "edit-delete")
        return Api.instance().icon(icon_name)
    
_ICON_NAME_MAP = {
    NodeType.PAINT_LAYER: "paintLayer",
    NodeType.GROUP_LAYER: "groupLayer",
    NodeType.FILE_LAYER: "fileLayer",
    NodeType.FILTER_LAYER: "filterLayer",
    NodeType.FILL_LAYER: "fillLayer",
    NodeType.CLONE_LAYER: "cloneLayer",
    NodeType.VECTOR_LAYER: "vectorLayer",
    NodeType.TRANSPARENCY_MASK: "transparencyMask",
    NodeType.FILTER_MASK: "filterMask",
    NodeType.TRANSFORM_MASK: "transformMask",
    NodeType.SELECTION_MASK: "selectionMask",
    NodeType.COLORIZE_MASK: "colorizeMask"
}
"""Maps node types to names of their icons."""