from dataclasses import dataclass
from typing import Protocol, Dict
from functools import cached_property
from krita import Krita as Api

from ..enums import BlendingMode


class KritaPreset(Protocol):
    def name(self) -> str: ...


class KritaView(Protocol):
    def currentBrushPreset(self) -> KritaPreset: ...
    def currentBlendingMode(self) -> str: ...
    def paintingOpacity(self) -> float: ...
    def paintingFlow(self) -> float: ...
    def brushSize(self) -> float: ...
    def setCurrentBrushPreset(self, preset: KritaPreset) -> None: ...
    def setCurrentBlendingMode(self, blending_mode: str) -> None: ...
    def setPaintingOpacity(self, opacity: int) -> None: ...
    def setPaintingFlow(self, flow: int) -> None: ...
    def setBrushSize(self, size: int) -> None: ...


@dataclass
class View:

    view: KritaView

    @cached_property
    def preset_map(self) -> Dict[str, KritaPreset]:
        return Api.instance().resources('preset')

    @property
    def brush_preset(self) -> str:
        return self.view.currentBrushPreset().name()

    @brush_preset.setter
    def brush_preset(self, preset_name: str) -> None:
        self.view.setCurrentBrushPreset(self.preset_map[preset_name])

    @property
    def blending_mode(self) -> BlendingMode:
        return BlendingMode(self.view.currentBlendingMode())

    @blending_mode.setter
    def blending_mode(self, mode: BlendingMode) -> None:
        self.view.setCurrentBlendingMode(mode.value)

    @property
    def opacity(self) -> int:
        return round(100*self.view.paintingOpacity())

    @opacity.setter
    def opacity(self, opacity: int) -> None:
        self.view.setPaintingOpacity(0.01*round(opacity))

    @property
    def flow(self) -> int:
        return round(100*self.view.paintingFlow())

    @flow.setter
    def flow(self, flow: int) -> None:
        self.view.setPaintingFlow(0.01*round(flow))

    @property
    def brush_size(self) -> float:
        return self.view.brushSize()

    @brush_size.setter
    def brush_size(self, brush_size: float) -> None:
        self.view.setBrushSize(brush_size)
