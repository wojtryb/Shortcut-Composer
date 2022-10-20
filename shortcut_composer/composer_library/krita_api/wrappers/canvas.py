from dataclasses import dataclass
from typing import Any


@dataclass
class Canvas:

    canvas: Any

    def rotation(self):
        return self.canvas.rotation()

    def set_rotation(self, angle_deg: float):
        self.canvas.setRotation(angle_deg)

    def zoom(self):
        return self.canvas.zoomLevel()

    def set_zoom(self, zoom: int):
        self.canvas.setZoomLevel(zoom)
