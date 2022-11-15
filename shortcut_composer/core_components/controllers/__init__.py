"""
Components that allow to get and set a specific property of krita.

Available controllers:
    - `ToolController`
    - `BrushSizeController`
    - `BlendingModeController`
    - `OpacityController`
    - `FlowController`
    - `PresetController`
    - `TimeController`
    - `LayerController`
    - `CanvasRotationController`
    - `CanvasZoomController`
    - `ToggleController`
"""

from .document_controllers import LayerController, TimeController
from .core_controllers import (
    ToggleController,
    ToolController,
    UndoController,
)
from .view_controllers import (
    BlendingModeController,
    BrushSizeController,
    OpacityController,
    PresetController,
    FlowController,
)
from .canvas_controllers import (
    CanvasRotationController,
    CanvasZoomController,
)

__all__ = [
    "CanvasRotationController",
    "BlendingModeController",
    "CanvasZoomController",
    "BrushSizeController",
    "OpacityController",
    "ToggleController",
    "PresetController",
    "LayerController",
    "TimeController",
    "ToolController",
    "UndoController",
    "FlowController",
]
