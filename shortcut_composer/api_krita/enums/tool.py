from enum import Enum

from krita import Krita as Api
from PyQt5.QtGui import QIcon


class Tool(Enum):
    """
    Contains all known tools from krita toolbox.

    Example usage: `Tool.FREEHAND_BRUSH`

    Available tools:
    - `FREEHAND_BRUSH`
    - `FREEHAND_SELECTION`
    - `GRADIENT`
    - `LINE`
    - `TRANSFORM`
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
    def is_paintable(tool: 'Tool'):
        """Is the user able to paint when the given tool is activated."""
        return tool in _PAINTABLE

    @property
    def icon(self) -> QIcon:
        icon_name = _ICON_MAP.get(self, "krita_tool_freehand")
        return Api.instance().icon(icon_name)


_PAINTABLE = {
    Tool.FREEHAND_BRUSH,
    Tool.LINE,
    Tool.ELLIPSE,
    Tool.DYNAMIC_BRUSH,
    Tool.RECTANGLE,
    Tool.MULTI_BRUSH,
    Tool.POLYLINE,
}

_ICON_MAP = {
    Tool.CROP: "tool_crop",
    Tool.PAN: "tool_pan",
    Tool.FREEHAND_SELECTION: "tool_outline_selection",
    Tool.FREEHAND_BRUSH: "krita_tool_freehand",
}
