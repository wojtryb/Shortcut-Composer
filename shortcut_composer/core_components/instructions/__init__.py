# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Components that allow to perform additional tasks outside the main logic.

Depending on the picked instruction, tasks can be performed on key
press, release, or in a loop while the key is pressed.

Available instructions:
    - `SetBrush`
    - `SetBrushOnNonPaintable`
    - `ToggleLayerVisibility`
    - `ToggleVisibilityAbove`
    - `UndoOnPress`
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
from .undo import UndoOnPress

__all__ = [
    'SetBrushOnNonPaintable',
    'ToggleLayerVisibility',
    'ToggleVisibilityAbove',
    'TemporaryOff',
    'TemporaryOn',
    'UndoOnPress',
    'EnsureOff',
    'EnsureOn',
    'SetBrush',
]
