# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Protocol
from functools import cached_property

from krita import Krita as Api

from ..enums import BlendingMode


class _KritaPreset(Protocol):
    """Krita `Resource` object API."""

    def name(self) -> str: ...


class KritaView(Protocol):
    """Krita `View` object API."""

    def currentBrushPreset(self) -> _KritaPreset: ...
    def currentBlendingMode(self) -> str: ...
    def paintingOpacity(self) -> float: ...
    def paintingFlow(self) -> float: ...
    def brushSize(self) -> float: ...
    def brushRotation(self) -> float: ...
    def setCurrentBrushPreset(self, preset: _KritaPreset) -> None: ...
    def setCurrentBlendingMode(self, blending_mode: str) -> None: ...
    def setPaintingOpacity(self, opacity: float) -> None: ...
    def setPaintingFlow(self, flow: float) -> None: ...
    def setBrushSize(self, size: float) -> None: ...
    def setBrushRotation(self, rotation: float) -> None: ...


@dataclass
class View:
    """Wraps krita `View` for typing, documentation and PEP8 compatibility."""

    view: KritaView

    @cached_property
    def preset_map(self) -> dict[str, _KritaPreset]:
        """Return dictionary mapping preset names to krita preset objects."""
        return Api.instance().resources('preset')

    @property
    def brush_preset(self) -> str:
        """Settable property with active brush preset name."""
        return self.view.currentBrushPreset().name()

    @brush_preset.setter
    def brush_preset(self, preset_name: str) -> None:
        """Set brush preset inside this `View` using its name."""
        if preset_name in self.preset_map:
            self.view.setCurrentBrushPreset(self.preset_map[preset_name])

    @property
    def blending_mode(self) -> BlendingMode:
        """Settable property with active blending mode enum."""
        return BlendingMode(self.view.currentBlendingMode())

    @blending_mode.setter
    def blending_mode(self, mode: BlendingMode) -> None:
        """Set blending mode inside this `View` using its enum."""
        self.view.setCurrentBlendingMode(mode.value)

    @property
    def opacity(self) -> int:
        """Settable property with painting opacity as %."""
        return round(100*self.view.paintingOpacity())

    @opacity.setter
    def opacity(self, opacity: int) -> None:
        """Set painting opacity inside this `View`."""
        self.view.setPaintingOpacity(0.01*round(opacity))

    @property
    def flow(self) -> int:
        """Settable property with painting flow as %."""
        return round(100*self.view.paintingFlow())

    @flow.setter
    def flow(self, flow: int) -> None:
        """Set painting flow inside this `View`."""
        self.view.setPaintingFlow(0.01*round(flow))

    @property
    def brush_size(self) -> float:
        """Settable property with brush size in pixels."""
        return self.view.brushSize()

    @brush_size.setter
    def brush_size(self, brush_size: float) -> None:
        """Set brush size inside this `View`."""
        self.view.setBrushSize(brush_size)

    @property
    def brush_rotation(self) -> float:
        """Settable property with brush rotation in deg between 0 and 360."""
        return self.view.brushRotation()

    @brush_rotation.setter
    def brush_rotation(self, rotation: float) -> None:
        """Set brush rotation with float representing angle in degrees."""
        self.view.setBrushRotation(rotation % 360)
