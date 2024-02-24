# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from typing import Protocol, Any

from .document import Document


class KritaCanvas(Protocol):
    """Krita `Canvas` object API."""

    def rotation(self) -> float: ...
    def setRotation(self, angle_deg: float) -> None: ...
    def zoomLevel(self) -> float: ...
    def setZoomLevel(self, zoom: float) -> None: ...
    def view(self) -> Any: ...


@dataclass
class Canvas:
    """Wraps krita `Canvas` for typing, docs and PEP8 compatibility."""

    canvas: KritaCanvas

    def __post_init__(self) -> None:
        self._zoom_scale = Document(self.canvas.view().document()).dpi/7200

    @property
    def rotation(self) -> float:
        """Settable property with rotation in degrees between `0` and `360`."""
        return self.canvas.rotation()

    @rotation.setter
    def rotation(self, angle_deg: float) -> None:
        """Set canvas rotation with float representing angle in degrees."""
        self.canvas.setRotation(angle_deg % 360)

    @property
    def zoom(self) -> float:
        """
        Settable property with zoom level expressed in %.

        Add a workaround for zoom detected by krita affected by document dpi.
        """
        return self.canvas.zoomLevel() / self._zoom_scale

    @zoom.setter
    def zoom(self, zoom: float) -> None:
        """Set zoom of canvas by providing zoom level expressed in %."""
        self.canvas.setZoomLevel(zoom*0.01)
