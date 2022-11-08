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

from .layer_hide import ToggleLayerVisibility
from .set_brush_strategy import SetBrush, SetBrushOnNonPaintable
from .togglers import (
    TemporaryOff,
    TemporaryOn,
    EnsureOff,
    EnsureOn,
)

__all__ = [
    'SetBrushOnNonPaintable',
    'ToggleLayerVisibility',
    'TemporaryOff',
    'TemporaryOn',
    'SetBrush',
    'EnsureOff',
    'EnsureOn',
]
