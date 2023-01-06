"""
Component that allows to get and set a specific property of krita.

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
from .canvas_controllers import (
    CanvasRotationController,
    CanvasZoomController)
from .core_controllers import (
    ToggleController,
    ToolController)
from .view_controllers import (
    BlendingModeController,
    BrushSizeController,
    OpacityController,
    PresetController,
    FlowController)

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
    "FlowController",
]
