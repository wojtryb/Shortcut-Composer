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

    @property
    def rotation(self) -> float:
        return self.canvas.rotation()

    @rotation.setter
    def rotation(self, angle_deg: float) -> None:
        self.canvas.setRotation(angle_deg)

    @property
    def zoom(self) -> float:
        return self.canvas.zoomLevel()

    @zoom.setter
    def zoom(self, zoom: int) -> None:
        self.canvas.setZoomLevel(zoom)
