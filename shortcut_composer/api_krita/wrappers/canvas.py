from dataclasses import dataclass
from typing import Protocol


class KritaCanvas(Protocol):
    def rotation(self) -> float: ...
    def setRotation(self, angle_deg: float) -> None: ...
    def zoomLevel(self) -> float: ...
    def setZoomLevel(self, zoom: float) -> None: ...


@dataclass
class Canvas:

    canvas: KritaCanvas

    def rotation(self) -> float:
        return self.canvas.rotation()

    def set_rotation(self, angle_deg: float) -> None:
        self.canvas.setRotation(angle_deg)

    def zoom(self) -> float:
        return self.canvas.zoomLevel()

    def set_zoom(self, zoom: int) -> None:
        self.canvas.setZoomLevel(zoom)
