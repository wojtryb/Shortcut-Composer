# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtGui import QPixmap, QImage, QColor
from api_krita import Krita
from api_krita.enums import BlendingMode
from api_krita.pyqt import PixmapTransform
from composer_utils.label import LabelText, LabelTextColorizer
from ..controller_base import Controller, NumericController


class ViewBasedController:
    """Family of controllers which operate on values from active view."""

    def refresh(self) -> None:
        """Refresh currently stored active view."""
        self.view = Krita.get_active_view()


class PresetController(ViewBasedController, Controller[str]):
    """
    Gives access to `presets`.

    - Operates on `string` representing name of preset
    - Does not have a default

    Example preset name: `"b) Basic-5 Size Opacity"`
    """

    TYPE = str
    REQUIRES_TEXT_SETTINGS = False

    def get_value(self) -> str:
        """Get currently active preset."""
        return self.view.brush_preset

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.view.brush_preset = value

    def get_label(self, value: str) -> QPixmap | None:
        """Return the preset icon or None, when there preset name unknown."""
        try:
            image: QImage = Krita.get_presets()[value].image()
        except KeyError:
            return None
        else:
            pixmap = QPixmap.fromImage(image)
            return PixmapTransform.make_pixmap_round(pixmap)


class BrushSizeController(ViewBasedController, NumericController):
    """
    Gives access to `brush size`.

    - Operates on `float` representing brush size in pixels
    - Defaults to `100`
    """

    TYPE = int
    REQUIRES_TEXT_SETTINGS = False
    DEFAULT_VALUE: int = 100
    MIN_VALUE = 1
    MAX_VALUE = 10_000
    STEP = 1
    WRAPPING = False
    ADAPTIVE = True

    def get_value(self) -> float:
        """Get current brush size."""
        return self.view.brush_size

    def set_value(self, value: float) -> None:
        """Set current brush size."""
        self.view.brush_size = value

    def get_label(self, value: float) -> LabelText:
        """Return LabelText with formatted brush size."""
        return LabelText(self.get_pretty_name(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the brush size like: `100px`"""
        return f"{round(value)}px"


class BrushRotationController(ViewBasedController, NumericController):
    """
    Gives access to `brush rotation` in degrees.

    - Operates on `int` in range `0 to 360`
    - Other values are expressed in that range
    - Defaults to `0`
    """

    TYPE = int
    REQUIRES_TEXT_SETTINGS = False
    DEFAULT_VALUE = 0
    MIN_VALUE = 0
    MAX_VALUE = 360
    STEP = 5
    WRAPPING = True
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get brush rotation in degrees."""
        return round(self.view.brush_rotation)

    def set_value(self, value: int) -> None:
        """Set brush rotation in degrees."""
        self.view.brush_rotation = value

    def get_label(self, value: int) -> LabelText:
        """Return Text with formatted canvas rotation."""
        return LabelText(self.get_pretty_name(value))

    def get_pretty_name(self, value: int) -> str:
        """Format the brush rotation like: `30°`."""
        return f"{round(value)}°"


class BlendingModeController(ViewBasedController, Controller[BlendingMode]):
    """
    Gives access to `brush blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    TYPE = BlendingMode
    REQUIRES_TEXT_SETTINGS = True
    DEFAULT_VALUE = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get currently active blending mode."""
        return self.view.blending_mode

    def set_value(self, value: BlendingMode) -> None:
        """Set a passed blending mode."""
        self.view.blending_mode = value

    def get_label(self, value: BlendingMode) -> LabelText:
        """Return Label of 3 first letters of mode name in correct color."""
        return LabelText(
            value=value.name,
            color=LabelTextColorizer.blending_mode(value))

    def get_pretty_name(self, value: BlendingMode) -> str:
        """Forward enums' pretty name."""
        return value.pretty_name


class OpacityController(ViewBasedController, NumericController):
    """
    Gives access to `brush opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    TYPE = int
    REQUIRES_TEXT_SETTINGS = False
    DEFAULT_VALUE: int = 100
    MIN_VALUE = 0
    MAX_VALUE = 100
    STEP = 1
    WRAPPING = False
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get current brush opacity."""
        return self.view.opacity

    def set_value(self, value: int) -> None:
        """Set passed brush opacity."""
        self.view.opacity = value

    def get_label(self, value: int) -> LabelText:
        """Return Text with formatted brush opacity."""
        return LabelText(
            value=self.get_pretty_name(value),
            color=LabelTextColorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the opacity like: `100%`"""
        return f"{value}%"


class FlowController(ViewBasedController, NumericController):
    """
    Gives access to `brush flow` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    TYPE = int
    REQUIRES_TEXT_SETTINGS = False
    DEFAULT_VALUE: int = 100
    MIN_VALUE = 0
    MAX_VALUE = 100
    STEP = 1
    WRAPPING = False
    ADAPTIVE = False

    def get_value(self) -> int:
        """Get current brush flow."""
        return self.view.flow

    def set_value(self, value: int) -> None:
        """Set passed brush flow."""
        self.view.flow = value

    def get_label(self, value: int) -> LabelText:
        """Return Text with formatted brush flow."""
        return LabelText(
            value=self.get_pretty_name(value),
            color=LabelTextColorizer.percentage(value))

    def get_pretty_name(self, value: float) -> str:
        """Format the flow like: `100%`"""
        return f"{value}%"


class ForegroundColorController(ViewBasedController, Controller[QColor]):
    """
    Gives access ForeGround painting color.

    - Operates on `QColor` class.
    - Defaults to black.
    """

    TYPE = QColor
    REQUIRES_TEXT_SETTINGS = False
    DEFAULT_VALUE: QColor = QColor(0, 0, 0, 255)

    def get_value(self) -> QColor:
        """Get current foreground color."""
        return self.view.foreground_color

    def set_value(self, value: QColor) -> None:
        """Set passed foreground color."""
        self.view.foreground_color = value

    def get_label(self, value: QColor) -> QColor:
        """Return the color itself, as QColor is a supported label."""
        return value

    def get_pretty_name(self, value: QColor) -> str:
        """Format the color like 'RGB(0, 0, 0)'."""
        return f"RGB({value.red()}, {value.green()}, {value.blue()})"
