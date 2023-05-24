# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Components that allow to get and set a specific property of krita.

Available controllers:
    - `ActionController`
    - `ToolController`
    - `BrushSizeController`
    - `BlendingModeController`
    - `OpacityController`
    - `FlowController`
    - `PresetController`
    - `TimeController`
    - `ActiveLayerController`
    - `LayerVisibilityController`
    - `LayerBlendingModeController`,
    - `LayerOpacityController`,
    - `CanvasRotationController`
    - `CanvasZoomController`
    - `ToggleController`
    - `CreateLayerWithBlendingController`
"""

from .document_controllers import (
    ActiveLayerController,
    TimeController,
)
from .canvas_controllers import (
    CanvasRotationController,
    CanvasZoomController,
)
from .view_controllers import (
    BlendingModeController,
    BrushSizeController,
    OpacityController,
    PresetController,
    FlowController,
)
from .node_controllers import (
    LayerBlendingModeController,
    LayerVisibilityController,
    LayerOpacityController,
    CreateLayerWithBlendingController,
)
from .core_controllers import (
    TransformModeController,
    ToggleController,
    ActionController,
    ToolController,
    UndoController,
)

__all__ = [
    "LayerBlendingModeController",
    "TransformModeController",
    "LayerVisibilityController",
    "CanvasRotationController",
    "BlendingModeController",
    "LayerOpacityController",
    "ActiveLayerController",
    "CanvasZoomController",
    "BrushSizeController",
    "OpacityController",
    "ToggleController",
    "PresetController",
    "ActionController",
    "TimeController",
    "ToolController",
    "UndoController",
    "FlowController",
    "CreateLayerWithBlendingController",
]
