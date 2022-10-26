from dataclasses import dataclass
from typing import Any

from ..enums import BlendingMode


@dataclass
class View:

    view: Any

    def current_brush_preset_name(self) -> str:
        return self.view.currentBrushPreset().name()

    def current_blending_mode(self) -> BlendingMode:
        return BlendingMode(self.view.currentBlendingMode())

    def current_opacity(self) -> int:
        return round(100*self.view.paintingOpacity())

    def current_flow(self) -> int:
        return round(100*self.view.paintingFlow())

    def current_brush_size(self) -> float:
        return self.view.brushSize()

    def set_brush_preset(self, preset) -> None:
        self.view.setCurrentBrushPreset(preset)

    def set_blending_mode(self, mode_name: BlendingMode) -> None:
        self.view.setCurrentBlendingMode(mode_name.value)

    def set_opacity(self, opacity: int) -> None:
        self.view.setPaintingOpacity(0.01*round(opacity))

    def set_flow(self, flow: int) -> None:
        self.view.setPaintingFlow(0.01*round(flow))

    def set_brush_size(self, brush_size: float) -> None:
        self.view.setBrushSize(brush_size)
