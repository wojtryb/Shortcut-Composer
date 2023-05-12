# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from enum import Enum

from PyQt5.QtGui import QIcon


class Tool(Enum):
    """
    Contains all known tools from krita toolbox.

    Extended with modes of the transform tool.

    Example usage: `Tool.FREEHAND_BRUSH`
    """

    SHAPE_SELECT = "InteractionTool"
    TEXT = "SvgTextTool"
    EDIT_SHAPES = "PathTool"
    CALLIGRAPHY = "KarbonCalligraphyTool"
    FREEHAND_BRUSH = "KritaShape/KisToolBrush"
    LINE = "KritaShape/KisToolLine"
    RECTANGLE = "KritaShape/KisToolRectangle"
    ELLIPSE = "KritaShape/KisToolEllipse"
    POLYGON = "KisToolPolygon"
    POLYLINE = "KisToolPolyline"
    BEZIER_PATH = "KisToolPath"
    FREEHAND_PATH = "KisToolPencil"
    DYNAMIC_BRUSH = "KritaShape/KisToolDyna"
    MULTI_BRUSH = "KritaShape/KisToolMultiBrush"
    TRANSFORM = "KisToolTransform"
    MOVE = "KritaTransform/KisToolMove"
    CROP = "KisToolCrop"
    GRADIENT = "KritaFill/KisToolGradient"
    COLOR_SAMPLER = "KritaSelected/KisToolColorSampler"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush"
    SMART_PATCH = "KritaShape/KisToolSmartPatch"
    FILL = "KritaFill/KisToolFill"
    ENCLOSE_AND_FILL = "KisToolEncloseAndFill"
    ASSISTANTS = "KisAssistantTool"
    MEASUREMENT = "KritaShape/KisToolMeasure"
    REFERENCE = "ToolReferenceImages"
    RECTANGULAR_SELECTION = "KisToolSelectRectangular"
    ELIPTICAL_SELECTION = "KisToolSelectElliptical"
    POLYGONAL_SELECTION = "KisToolSelectPolygonal"
    FREEHAND_SELECTION = "KisToolSelectOutline"
    CONTIGUOUS_SELECTION = "KisToolSelectContiguous"
    SIMILAR_COLOR_SELECTION = "KisToolSelectSimilar"
    BEZIER_SELECTION = "KisToolSelectPath"
    MAGNETIC_SELECTION = "KisToolSelectMagnetic"
    ZOOM = "ZoomTool"
    PAN = "PanTool"

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

    @property
    def pretty_name(self) -> str:
        """Format tool name like: `Shape select tool`."""
        return f"{self.name[0]}{self.name[1:].lower().replace('_', ' ')} tool"


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
    Tool.TRANSFORM: "krita_tool_transform",
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
    Tool.COLOR_SAMPLER: "krita_tool_color_sampler",
    Tool.POLYGON: "krita_tool_polygon",
    Tool.MEASUREMENT: "krita_tool_measure",
    Tool.TEXT: "draw-text",
    Tool.ELLIPSE: "krita_tool_ellipse",
    Tool.FILL: "krita_tool_color_fill",
    Tool.ENCLOSE_AND_FILL: "krita_tool_enclose_and_fill",
    Tool.BEZIER_SELECTION: "tool_path_selection",
    Tool.DYNAMIC_BRUSH: "krita_tool_dyna",
    Tool.RECTANGLE: "krita_tool_rectangle",
    Tool.PAN: "tool_pan",
    Tool.MULTI_BRUSH: "krita_tool_multihand",
    Tool.EDIT_SHAPES: "shape_handling",
    Tool.ELIPTICAL_SELECTION: "tool_elliptical_selection",
    Tool.SMART_PATCH: "krita_tool_smart_patch",
    Tool.COLORIZE_MASK: "krita_tool_lazybrush",
    Tool.SIMILAR_COLOR_SELECTION: "tool_similar_selection",
    Tool.ZOOM: "tool_zoom",
    Tool.MAGNETIC_SELECTION: "tool_magnetic_selection",
    Tool.CALLIGRAPHY: "calligraphy",
    Tool.POLYGONAL_SELECTION: "tool_polygonal_selection"
}
"""Maps tools to names of their icons."""
