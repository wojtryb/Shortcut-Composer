# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from enum import Enum

from PyQt5.QtGui import QIcon


class Tool(Enum):
    """
    Contains all known tools from krita toolbox.

    Extended with modes of the transform tool.

    Example usage: `Tool.FREEHAND_BRUSH`

    Available tools:
    - `FREEHAND_BRUSH`
    - `FREEHAND_SELECTION`
    - `GRADIENT`
    - `LINE`
    - `TRANSFORM`
    - `TRANSFORM_FREE`
    - `TRANSFORM_PERSPECTIVE`
    - `TRANSFORM_WARP`
    - `TRANSFORM_CAGE`
    - `TRANSFORM_LIQUIFY`
    - `TRANSFORM_MESH`
    - `MOVE`
    - `RECTANGULAR_SELECTION`
    - `CONTIGUOUS_SELECTION`
    - `REFERENCE`
    - `CROP`
    - `BEZIER_PATH`
    - `FREEHAND_PATH`
    - `POLYLINE`
    - `SHAPE_SELECT`
    - `ASSISTANTS`
    - `COLOR_SAMPLER`
    - `POLYGON`
    - `MEASUREMENT`
    - `TEXT`
    - `ELLIPSE`
    - `FILL`
    - `BEZIER_SELECTION`
    - `DYNAMIC_BRUSH`
    - `RECTANGLE`
    - `PAN`
    - `MULTI_BRUSH`
    - `EDIT_SHAPES`
    - `ELIPTICAL_SELECTION`
    - `SMART_PATCH`
    - `COLORIZE_MASK`
    - `SIMILAR_COLOR_SELECTION`
    - `ZOOM`
    - `MAGNETIC_SELECTION`
    - `CALLIGRAPHY`
    - `POLYGONAL_SELECTION`
    """

    FREEHAND_BRUSH = "KritaShape/KisToolBrush"
    FREEHAND_SELECTION = "KisToolSelectOutline"
    GRADIENT = "KritaFill/KisToolGradient"
    LINE = "KritaShape/KisToolLine"
    TRANSFORM = "KisToolTransform"
    TRANSFORM_FREE = "Transform tool: free"
    TRANSFORM_PERSPECTIVE = "Transform tool: perspective"
    TRANSFORM_WARP = "Transform tool: warp"
    TRANSFORM_CAGE = "Transform tool: cage"
    TRANSFORM_LIQUIFY = "Transform tool: liquify"
    TRANSFORM_MESH = "Transform tool: mesh"
    MOVE = "KritaTransform/KisToolMove"
    RECTANGULAR_SELECTION = "KisToolSelectRectangular"
    CONTIGUOUS_SELECTION = "KisToolSelectContiguous"
    REFERENCE = "ToolReferenceImages"
    CROP = "KisToolCrop"
    BEZIER_PATH = "KisToolPath"
    FREEHAND_PATH = "KisToolPencil"
    POLYLINE = "KisToolPolyline"
    SHAPE_SELECT = "InteractionTool"
    ASSISTANTS = "KisAssistantTool"
    COLOR_SAMPLER = "KritaSelected/KisToolColorSampler"
    POLYGON = "KisToolPolygon"
    MEASUREMENT = "KritaShape/KisToolMeasure"
    TEXT = "SvgTextTool"
    ELLIPSE = "KritaShape/KisToolEllipse"
    FILL = "KritaFill/KisToolFill"
    BEZIER_SELECTION = "KisToolSelectPath"
    DYNAMIC_BRUSH = "KritaShape/KisToolDyna"
    RECTANGLE = "KritaShape/KisToolRectangle"
    PAN = "PanTool"
    MULTI_BRUSH = "KritaShape/KisToolMultiBrush"
    EDIT_SHAPES = "PathTool"
    ELIPTICAL_SELECTION = "KisToolSelectElliptical"
    SMART_PATCH = "KritaShape/KisToolSmartPatch"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush"
    SIMILAR_COLOR_SELECTION = "KisToolSelectSimilar"
    ZOOM = "ZoomTool"
    MAGNETIC_SELECTION = "KisToolSelectMagnetic"
    CALLIGRAPHY = "KarbonCalligraphyTool"
    POLYGONAL_SELECTION = "KisToolSelectPolygonal"

    def activate(self):
        Api.instance().action(self.value).trigger()

    @staticmethod
    def is_paintable(tool: 'Tool') -> bool:
        """Is the user able to paint when the given tool is activated."""
        return tool in _PAINTABLE

    @property
    def icon(self) -> QIcon:
        """Return the icon of this tool."""
        icon_name = _ICON_NAME_MAP.get(self, "edit-delete")
        return Api.instance().icon(icon_name)

    def __eq__(self, other) -> bool:
        """All subtools of transform tool are technically the same tool."""
        if self in _TRANSFORMS and other in _TRANSFORMS:
            return True
        return Enum.__eq__(self, other)

    def __hash__(self) -> int:
        """Identify tool by its krita name."""
        return hash(self.value)


_TRANSFORMS = {
    Tool.TRANSFORM,
    Tool.TRANSFORM_FREE,
    Tool.TRANSFORM_PERSPECTIVE,
    Tool.TRANSFORM_WARP,
    Tool.TRANSFORM_CAGE,
    Tool.TRANSFORM_LIQUIFY,
    Tool.TRANSFORM_MESH,
}
"""Set of all subtools that are in fact the transform tool."""

_PAINTABLE = {
    Tool.FREEHAND_BRUSH,
    Tool.LINE,
    Tool.ELLIPSE,
    Tool.DYNAMIC_BRUSH,
    Tool.RECTANGLE,
    Tool.MULTI_BRUSH,
    Tool.POLYLINE,
}
"""Set of tools that are used to paint on the canvas."""

_ICON_NAME_MAP = {
    Tool.FREEHAND_BRUSH: "krita_tool_freehand",
    Tool.FREEHAND_SELECTION: "tool_outline_selection",
    Tool.GRADIENT: "krita_tool_gradient",
    Tool.LINE: "krita_tool_line",
    Tool.TRANSFORM_FREE: "krita_tool_transform",
    Tool.TRANSFORM_PERSPECTIVE: "transform_icons_perspective",
    Tool.TRANSFORM_WARP: "transform_icons_warp",
    Tool.TRANSFORM_CAGE: "transform_icons_cage",
    Tool.TRANSFORM_LIQUIFY: "transform_icons_liquify_main",
    Tool.TRANSFORM_MESH: "transform_icons_mesh",
    Tool.MOVE: "krita_tool_move",
    Tool.RECTANGULAR_SELECTION: "tool_rect_selection",
    Tool.CONTIGUOUS_SELECTION: "tool_contiguous_selection",
    Tool.REFERENCE: "krita_tool_reference_images",
    Tool.CROP: "tool_crop",
    Tool.BEZIER_PATH: "krita_draw_path",
    Tool.FREEHAND_PATH: "krita_tool_freehandvector",
    Tool.POLYLINE: "polyline",
    Tool.SHAPE_SELECT: "select",
    Tool.ASSISTANTS: "krita_tool_assistant",
    Tool.COLOR_SAMPLER: "krita_tool_color_picker",
    Tool.POLYGON: "krita_tool_polygon",
    Tool.MEASUREMENT: "krita_tool_measure",
    Tool.TEXT: "draw-text",
    Tool.ELLIPSE: "krita_tool_ellipse",
    Tool.FILL: "krita_tool_color_fill",
    Tool.BEZIER_SELECTION: "tool_path_selection",
    Tool.DYNAMIC_BRUSH: "krita_tool_dyna",
    Tool.RECTANGLE: "krita_tool_rectangle",
    Tool.PAN: "tool_pan",
    Tool.MULTI_BRUSH: "krita_tool_multihand",
    Tool.EDIT_SHAPES: "shape_handling",
    Tool.ELIPTICAL_SELECTION: "tool_elliptical_selection",
    Tool.SMART_PATCH: "krita_tool_smart_patch",
    Tool.COLORIZE_MASK: "colorizeMask",
    Tool.SIMILAR_COLOR_SELECTION: "tool_similar_selection",
    Tool.ZOOM: "tool_zoom",
    Tool.MAGNETIC_SELECTION: "tool_magnetic_selection",
    Tool.CALLIGRAPHY: "calligraphy",
    Tool.POLYGONAL_SELECTION: "tool_polygonal_selection"
}
"""Maps tools to names of their icons."""
