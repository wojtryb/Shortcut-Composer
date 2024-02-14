# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.enums import Tool
from ..instruction_base import Instruction


class SetBrush(Instruction):
    """
    Switches current tool to `Tool.FREEHAND_BRUSH` on each key press.

    ### Usage example:
    ```python
    instructions.SetBrush()
    ```
    """

    def on_key_press(self) -> None:
        Krita.trigger_action(Tool.FREEHAND_BRUSH.value)


class SetBrushOnNonPaintable(Instruction):
    """
    Switches current tool to `Tool.FREEHAND_BRUSH` on key press if
    current tool does not allow to paint.

    Tools that do allow to paint:
    - `Tool.FREEHAND_BRUSH`,
    - `Tool.LINE`,
    - `Tool.ELLIPSE`,
    - `Tool.DYNAMIC_BRUSH`,
    - `Tool.RECTANGLE`,
    - `Tool.MULTI_BRUSH`,
    - `Tool.POLYLINE`,

    ### Usage example:
    ```python
    instructions.SetBrushOnNonPaintable()
    ```
    """

    def on_key_press(self) -> None:
        if not Tool.is_paintable(Krita.active_tool):
            Krita.trigger_action(Tool.FREEHAND_BRUSH.value)
