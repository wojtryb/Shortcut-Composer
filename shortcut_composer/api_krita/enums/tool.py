# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from PyQt5.QtGui import QIcon

from .helpers import EnumGroup, Group


class Tool(EnumGroup):

    _vectors = Group("Vectors")
    SHAPE_SELECT = "InteractionTool"
    TEXT = "SvgTextTool"
    EDIT_SHAPES = "PathTool"
    CALLIGRAPHY = "KarbonCalligraphyTool"

    _painting = Group("Painting")
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

    _editing = Group("Editing")
    TRANSFORM = "KisToolTransform"
    MOVE = "KritaTransform/KisToolMove"
    CROP = "KisToolCrop"
    GRADIENT = "KritaFill/KisToolGradient"
    COLOR_SAMPLER = "KritaSelected/KisToolColorSampler"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush"
    SMART_PATCH = "KritaShape/KisToolSmartPatch"
    FILL = "KritaFill/KisToolFill"
    ENCLOSE_AND_FILL = "KisToolEncloseAndFill"

    _utility = Group("Utility")
    ASSISTANTS = "KisAssistantTool"
    MEASUREMENT = "KritaShape/KisToolMeasure"
    REFERENCE = "ToolReferenceImages"

    _selection = Group("Selection")
    RECTANGULAR_SELECTION = "KisToolSelectRectangular"
    ELIPTICAL_SELECTION = "KisToolSelectElliptical"
    POLYGONAL_SELECTION = "KisToolSelectPolygonal"
    FREEHAND_SELECTION = "KisToolSelectOutline"
    CONTIGUOUS_SELECTION = "KisToolSelectContiguous"
    SIMILAR_COLOR_SELECTION = "KisToolSelectSimilar"
    BEZIER_SELECTION = "KisToolSelectPath"
    MAGNETIC_SELECTION = "KisToolSelectMagnetic"

    _canvas_navigation = Group("Canvas navigation")
    ZOOM = "ZoomTool"
    PAN = "PanTool"

    @property
    def pretty_name(self) -> str:
        """Format tool name as in Krita Blending Mode combobox."""
        if self in PRETTY_NAMES:
            return PRETTY_NAMES[self]
        return f"{self.name.replace('_', ' ').title()} Tool"

    def activate(self) -> None:
        Api.instance().action(self.value).trigger()

    @classmethod
    def is_paintable(cls, tool: 'Tool') -> bool:
        """Is the user able to paint when the given tool is activated."""
        return tool in cls._painting  # type: ignore

    @property
    def icon(self) -> QIcon:
        """Return the icon of this tool."""
        return Api.instance().action(self.value).icon()


PRETTY_NAMES = {
    Tool.SHAPE_SELECT: "Select Shapes Tool",
    Tool.CALLIGRAPHY: "Calligraphy",
    Tool.COLOR_SAMPLER: "Color Sampler",
    Tool.ENCLOSE_AND_FILL: "Enclose and Fill Tool",
    Tool.ASSISTANTS: "Assistant Tool",
    Tool.REFERENCE: "Reference Images Tool",
}
