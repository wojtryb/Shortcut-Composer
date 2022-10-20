from enum import Enum


class Tools(Enum):
    freehand_brush = "KritaShape/KisToolBrush"
    freehand_selection = "KisToolSelectOutline"
    gradient = "KritaFill/KisToolGradient"
    line = "KritaShape/KisToolLine"
    transform = "KisToolTransform"
    move = "KritaTransform/KisToolMove"
    rectangular_selection = "KisToolSelectRectangular"
    contiquous_selection = "KisToolSelectContiguous"
    reference = "ToolReferenceImages"


class BlendingModes(Enum):
    normal = "normal"
    overlay = "overlay"
