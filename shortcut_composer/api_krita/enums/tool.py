# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api

from typing import Optional
from PyQt5.QtGui import QIcon
from .helpers import EnumGroup, Group


class Tool(EnumGroup):

    _vectors = Group("Vectors")
    SHAPE_SELECT = "InteractionTool", "Select Shapes Tool"
    TEXT = "SvgTextTool"
    EDIT_SHAPES = "PathTool"
    CALLIGRAPHY = "KarbonCalligraphyTool", "Calligraphy"

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
    COLOR_SAMPLER = "KritaSelected/KisToolColorSampler", "Color Sampler"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush"
    SMART_PATCH = "KritaShape/KisToolSmartPatch"
    FILL = "KritaFill/KisToolFill"
    ENCLOSE_AND_FILL = "KisToolEncloseAndFill", "Enclose and Fill Tool"

    _utility = Group("Utility")
    ASSISTANTS = "KisAssistantTool", "Assistant Tool"
    MEASUREMENT = "KritaShape/KisToolMeasure"
    REFERENCE = "ToolReferenceImages", "Reference Images Tool"

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

    def __init__(self, value: str, pretty_name: Optional[str] = None):
        self._value_ = value
        self._custom_pretty_name = pretty_name

    @property
    def pretty_name(self) -> str:
        """Format tool name as in Krita Blending Mode combobox."""
        if self._custom_pretty_name is not None:
            return self._custom_pretty_name
        return f"{self.name.replace('_', ' ').title()} Tool"

    def activate(self):
        Api.instance().action(self.value).trigger()

    @classmethod
    def is_paintable(cls, tool: 'Tool') -> bool:
        """Is the user able to paint when the given tool is activated."""
        return tool in cls._painting  # type: ignore

    @property
    def icon(self) -> QIcon:
        """Return the icon of this tool."""
        return Api.instance().action(self.value).icon()
