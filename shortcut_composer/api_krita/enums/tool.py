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

    FREEHAND_BRUSH = "KritaShape/KisToolBrush", "krita_tool_freehand"
    FREEHAND_SELECTION = "KisToolSelectOutline", "tool_outline_selection"
    GRADIENT = "KritaFill/KisToolGradient", "krita_tool_gradient"
    LINE = "KritaShape/KisToolLine", "krita_tool_line"
    TRANSFORM = "KisToolTransform", "krita_tool_transform"
    MOVE = "KritaTransform/KisToolMove", "krita_tool_move"
    RECTANGULAR_SELECTION = "KisToolSelectRectangular", "tool_rect_selection"
    CONTIGUOUS_SELECTION = ("KisToolSelectContiguous",
                            "tool_contiguous_selection")
    REFERENCE = "ToolReferenceImages", "krita_tool_reference_images"
    CROP = "KisToolCrop", "tool_crop"
    BEZIER_PATH = "KisToolPath", "krita_draw_path"
    FREEHAND_PATH = "KisToolPencil", "krita_tool_freehandvector"
    POLYLINE = "KisToolPolyline", "polyline"
    SHAPE_SELECT = "InteractionTool", "select"
    ASSISTANTS = "KisAssistantTool", "krita_tool_assistant"
    COLOR_SAMPLER = ("KritaSelected/KisToolColorSampler",
                     "krita_tool_color_picker")
    POLYGON = "KisToolPolygon", "krita_tool_polygon"
    MEASUREMENT = "KritaShape/KisToolMeasure", "krita_tool_measure"
    TEXT = "SvgTextTool", "draw-text"
    ELLIPSE = "KritaShape/KisToolEllipse", "krita_tool_ellipse"
    FILL = "KritaFill/KisToolFill", "krita_tool_color_fill"
    BEZIER_SELECTION = "KisToolSelectPath", "tool_path_selection"
    DYNAMIC_BRUSH = "KritaShape/KisToolDyna", "krita_tool_dyna"
    RECTANGLE = "KritaShape/KisToolRectangle", "krita_tool_rectangle"
    PAN = "PanTool", "tool_pan"
    MULTI_BRUSH = "KritaShape/KisToolMultiBrush", "krita_tool_multihand"
    EDIT_SHAPES = "PathTool", "shape_handling"
    ELIPTICAL_SELECTION = ("KisToolSelectElliptical",
                           "tool_elliptical_selection")
    SMART_PATCH = "KritaShape/KisToolSmartPatch", "krita_tool_smart_patch"
    COLORIZE_MASK = "KritaShape/KisToolLazyBrush", "colorizeMask"
    SIMILAR_COLOR_SELECTION = "KisToolSelectSimilar", "tool_similar_selection"
    ZOOM = "ZoomTool", "tool_zoom"
    MAGNETIC_SELECTION = "KisToolSelectMagnetic", "tool_magnetic_selection"
    CALLIGRAPHY = "KarbonCalligraphyTool", "calligraphy"
    POLYGONAL_SELECTION = "KisToolSelectPolygonal", "tool_polygonal_selection"

    def activate(self):
        Api.instance().action(super().value[0]).trigger()

    @staticmethod
    def is_paintable(tool: 'Tool'):
        """Is the user able to paint when the given tool is activated."""
        return tool in _PAINTABLE

    @property
    def value(self):
        super().value[0]

    @property
    def icon(self) -> QIcon:
        return Api.instance().icon(super().value[1])


_PAINTABLE = {
    Tool.FREEHAND_BRUSH,
    Tool.LINE,
    Tool.ELLIPSE,
    Tool.DYNAMIC_BRUSH,
    Tool.RECTANGLE,
    Tool.MULTI_BRUSH,
    Tool.POLYLINE,
}
