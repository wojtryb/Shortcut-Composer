"""
Components that allow to perform additional tasks outside the main logic.

Depending on the picked instruction, tasks can be performed on key
press, release, or in a loop while the key is pressed.

Available instructions:
    - `SetBrush`
    - `SetBrushOnNonPaintable`
    - `ToggleLayerVisibility`
    - `ToggleVisibilityAbove`
    - `EnsureOn`
    - `EnsureOff`
    - `TemporaryOn`
    - `TemporaryOff`
"""

from .layer_hide import ToggleLayerVisibility, ToggleVisibilityAbove
from .set_brush_strategy import SetBrush, SetBrushOnNonPaintable
from .togglers import (
    TemporaryOff,
    TemporaryOn,
    EnsureOff,
    EnsureOn,
)
from .undo import UndoOnShortPress

__all__ = [
    'SetBrushOnNonPaintable',
    'ToggleLayerVisibility',
    'ToggleVisibilityAbove',
    'UndoOnShortPress',
    'TemporaryOff',
    'TemporaryOn',
    'SetBrush',
    'EnsureOff',
    'EnsureOn',
]
