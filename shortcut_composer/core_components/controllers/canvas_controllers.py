# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from composer_utils.label import LabelText

from ..controller_base import NumericController


class CanvasBasedController:
    """Family of controllers which operate on values from active document."""

    def refresh(self) -> None:
        """Refresh currently stored canvas."""
        self.canvas = Krita.get_active_canvas()


class CanvasZoomController(CanvasBasedController, NumericController):
    """
    Gives access to `zoom` in %.

    - Operates on `int`
    - Defaults to `100`
    """

    TYPE = int
    DEFAULT_VALUE = 100
    MIN_VALUE = 1
    MAX_VALUE = 6_400
    STEP = 1
    WRAPPING = False
    ADAPTIVE = True

    def get_value(self) -> int:
        """Get current zoom level in %"""
        return round(self.canvas.zoom)

    def set_value(self, value: int) -> None:
        """Set current zoom level in %"""
        self.canvas.zoom = value

    def get_label(self, value: int) -> LabelText:
        """Return LabelText with formatted canvas zoom."""
        return LabelText(self.get_pretty_name(value))

    def get_pretty_name(self, value: int) -> str:
        """Format the canvas zoom like: `100%`."""
        return f"{round(value)}%"


class CanvasRotationController(CanvasBasedController, NumericController):
    """
    Gives access to `canvas rotation` in degrees.

    - Operates on `int` in range `0 to 360`
    - Other values are expressed in that range
    - Defaults to `0`
    """

    TYPE = int
    DEFAULT_VALUE = 0
    MIN_VALUE = 0
    MAX_VALUE = 360
    STEP = 5
    WRAPPING = True
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get canvas rotation in degrees."""
        return round(self.canvas.rotation)

    def set_value(self, value: int) -> None:
        """Set rotation in degrees."""
        self.canvas.rotation = value

    def get_label(self, value: int) -> LabelText:
        """Return LabelText with formatted canvas rotation."""
        return LabelText(self.get_pretty_name(value))

    def get_pretty_name(self, value: int) -> str:
        """Format the canvas rotation like: `30°`."""
        return f"{round(value)}°"
