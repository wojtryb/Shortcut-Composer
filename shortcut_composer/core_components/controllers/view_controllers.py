# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QPixmap, QImage

from api_krita import Krita
from api_krita.enums import BlendingMode
from api_krita.pyqt import Text, Colorizer
from ..controller_base import Controller


class ViewBasedController(Controller):
    """Family of controllers which operate on values from active view."""

    def refresh(self):
        """Refresh currently stored active view."""
        self.view = Krita.get_active_view()


class PresetController(ViewBasedController):
    """
    Gives access to `presets`.

    - Operates on `string` representing name of preset
    - Does not have a default

    Example preset name: `"b) Basic-5 Size Opacity"`
    """

    def get_value(self) -> str:
        """Get currently active preset."""
        return self.view.brush_preset

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.view.brush_preset = value

    def get_label(self, value: str) -> QPixmap:
        image: QImage = Krita.get_presets()[value].image()
        return QPixmap.fromImage(image)


class BrushSizeController(ViewBasedController):
    """
    Gives access to `brush size`.

    - Operates on `float` representing brush size in pixels
    - Defaults to `100`
    """

    default_value: float = 100

    def get_value(self) -> float:
        return self.view.brush_size

    def set_value(self, value: float) -> None:
        self.view.brush_size = value

    def get_label(self, value: float) -> Text:
        return Text(f"{round(value)}px")


class BlendingModeController(ViewBasedController):
    """
    Gives access to `brush blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get currently active blending mode."""
        return self.view.blending_mode

    def set_value(self, value: BlendingMode) -> None:
        """Set a passed blending mode."""
        self.view.blending_mode = value

    def get_label(self, value: BlendingMode) -> Text:
        return Text(value.name[:3], Colorizer.blending_mode(value))


class OpacityController(ViewBasedController):
    """
    Gives access to `brush opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get current brush opacity."""
        return self.view.opacity

    def set_value(self, value: int) -> None:
        """Set passed brush opacity."""
        self.view.opacity = value

    def get_label(self, value: int) -> Text:
        return Text(f"{value}%", Colorizer.percentage(value))


class FlowController(ViewBasedController):
    """
    Gives access to `brush flow` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        return self.view.flow

    def set_value(self, value: int) -> None:
        self.view.flow = value

    def get_label(self, value: int) -> Text:
        return Text(f"{value}%", Colorizer.percentage(value))
