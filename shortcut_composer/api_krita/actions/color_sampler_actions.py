# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QWidget,
    QSpinBox,
)

from ..enums import Tool
from ..core_api import KritaInstance
Krita = KritaInstance()


class ColorSamplerOptionsFinder:
    """
    Helper class for finding components related to Color Sampler Tool.

    Stores elements of krita needed to control Color Sampler Tool:
    - Widget Color Sampler tool options
    - Blend property of Color Sampler

    As the widget do not exist during plugin intialization phase,
    fetching the elements needs to happen at runtime.
    """

    def __init__(self) -> None:
        self._initialized = False

        self._color_sampler_options: QWidget
        self._blend_spinbox: QSpinBox

    def ensure_initialized(self) -> None:
        """Fetch widget and blend spinbox if not done already."""
        if not self._initialized:
            last_tool = Krita.active_tool
            Krita.active_tool = Tool.COLOR_SAMPLER
            self._color_sampler_options = self._fetch_color_sampler_options()
            self._blend_spinbox = self._fetch_blend_spinbox()
            self._initialized = True
            Krita.active_tool = last_tool

    def set_blend(self, blend: int) -> None:
        """Set Color Sampler Blend percentage."""
        self.ensure_initialized()

        last_tool = Krita.active_tool
        Krita.active_tool = Tool.COLOR_SAMPLER

        blend = sorted((1, blend, 100))[1]
        self._blend_spinbox.setValue(blend)

        Krita.active_tool = last_tool

    def get_blend(self) -> int:
        """Get Color Sampler Blend percentage."""
        self.ensure_initialized()
        return self._blend_spinbox.value()

    def _fetch_color_sampler_options(self) -> QWidget:
        """Fetch widget with Color Sampler tool options."""
        for qobj in Krita.get_active_qwindow().findChildren(QWidget):
            if qobj.objectName() == (
                Tool.COLOR_SAMPLER.value + " option widget"):
                return qobj  # type: ignore
        raise RuntimeError("Color Sampler options not found.")

    def _fetch_blend_spinbox(self) -> QSpinBox:
        """Fetch Color Sampler tool Blend property SpinBox widget."""
        blend_spinbox_list = self._color_sampler_options.findChildren(QSpinBox)
        if not blend_spinbox_list:
            raise RuntimeError("Could not ifnd the Blend SpinBox.")
        for qobj in blend_spinbox_list:
            if qobj.objectName() == "blend":
                return qobj # type: ignore

