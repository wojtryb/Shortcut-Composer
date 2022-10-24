from enum import Enum


class Tool(Enum):
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

    @staticmethod
    def is_paintable(tool: 'Tool'):
        return tool in _PAINTABLE


_PAINTABLE = {
    Tool.FREEHAND_BRUSH,
    Tool.LINE,
    Tool.ELLIPSE,
    Tool.DYNAMIC_BRUSH,
    Tool.RECTANGLE,
    Tool.MULTI_BRUSH,
    Tool.POLYLINE,
}
