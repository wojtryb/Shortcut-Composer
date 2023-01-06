"""
Components that allow to perform additional tasks outside the main logic.

Depending on the picked instruction, tasks can be performed on key
press, release, or in a loop while the key is pressed.

Available instructions:
    - `SetBrush`
    - `SetBrushOnNonPaintable`
    - `ToggleLayerVisibility`
    - `EnsureOn`
    - `EnsureOff`
    - `TemporaryOn`
    - `TemporaryOff`
"""

from .layer_hide import ToggleLayerVisibility, ToggleShowBelow
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
    'ToggleShowBelow',
    'TemporaryOff',
    'TemporaryOn',
    'UndoOnShortPress',
    'SetBrush',
    'EnsureOff',
    'EnsureOn',
]
