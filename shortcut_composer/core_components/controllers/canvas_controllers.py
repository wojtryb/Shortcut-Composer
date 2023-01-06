# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita import Krita
from api_krita.pyqt import Text
from ..controller_base import Controller


class CanvasBasedController(Controller):
    """Family of controllers which operate on values from active document."""

    def refresh(self):
        """Refresh currently stored canvas."""
        self.canvas = Krita.get_active_canvas()


class CanvasZoomController(CanvasBasedController):
    """
    Gives access to `zoom`.

    - Operates on `float`
    - Defaults to `1.0`
    """

    default_value: float = 100.0

    def get_value(self) -> float:
        return self.canvas.zoom

    def set_value(self, value: float) -> None:
        self.canvas.zoom = value

    def get_label(self, value: float) -> Text:
        return Text(f"{round(value/100, 2)}")


class CanvasRotationController(CanvasBasedController):
    """
    Gives access to `canvas rotation` in degrees.

    - Operates on `float` in range `0.0 to 360.0`
    - Other values are expressed in that range
    - Defaults to `0.0`
    """

    default_value: float = 0.0

    def get_value(self) -> float:
        return self.canvas.rotation

    def set_value(self, value: float) -> None:
        self.canvas.rotation = value

    def get_label(self, value: float) -> Text:
        return Text(f"{round(value)}°")
