# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from enum import Enum

from PyQt5.QtGui import QIcon


class TransformMode(Enum):
    """
    Contains all known tools from krita toolbox.

    Extended with modes of the transform tool.

    Example usage: `Tool.FREEHAND_BRUSH`

    Available tools:
    - `TRANSFORM_FREE`
    - `TRANSFORM_PERSPECTIVE`
    - `TRANSFORM_WARP`
    - `TRANSFORM_CAGE`
    - `TRANSFORM_LIQUIFY`
    - `TRANSFORM_MESH`
"""

    FREE = "Transform tool: free"
    PERSPECTIVE = "Transform tool: perspective"
    WARP = "Transform tool: warp"
    CAGE = "Transform tool: cage"
    LIQUIFY = "Transform tool: liquify"
    MESH = "Transform tool: mesh"

    def activate(self) -> None:
        Api.instance().action(self.value).trigger()

    @property
    def button_name(self) -> str:
        return _BUTTONS_MAP[self]

    @property
    def icon(self) -> QIcon:
        """Return the icon of this tool."""
        icon_name = _ICON_NAME_MAP.get(self, "edit-delete")
        return Api.instance().icon(icon_name)


_ICON_NAME_MAP = {
    TransformMode.FREE: "krita_tool_transform",
    TransformMode.PERSPECTIVE: "transform_icons_perspective",
    TransformMode.WARP: "transform_icons_warp",
    TransformMode.CAGE: "transform_icons_cage",
    TransformMode.LIQUIFY: "transform_icons_liquify_main",
    TransformMode.MESH: "transform_icons_mesh",
}

_BUTTONS_MAP = {
    TransformMode.FREE: "freeTransformButton",
    TransformMode.PERSPECTIVE: "perspectiveTransformButton",
    TransformMode.WARP: "warpButton",
    TransformMode.CAGE: "cageButton",
    TransformMode.LIQUIFY: "liquifyButton",
    TransformMode.MESH: "meshButton",
}
"""Maps the TransformMode Tools to their buttons from the widget."""
