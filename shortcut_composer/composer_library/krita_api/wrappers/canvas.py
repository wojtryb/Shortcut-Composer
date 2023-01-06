from dataclasses import dataclass
from typing import Any


@dataclass
class Canvas:

    canvas: Any

    def rotation(self) -> float:
        return self.canvas.rotation()

    def set_rotation(self, angle_deg: float) -> None:
        self.canvas.setRotation(angle_deg)

    def zoom(self) -> float:
        return self.canvas.zoomLevel()

    def set_zoom(self, zoom: int) -> None:
        self.canvas.setZoomLevel(zoom)
