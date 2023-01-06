from api_krita import Krita
from ..controller_base import Controller


class CanvasBasedController(Controller):

    def refresh(self):
        self.canvas = Krita.get_active_canvas()


class CanvasZoomController(CanvasBasedController):
    """
    Gives access to zoom.

    - Operates on floats
    - Defaults to 1.0
    """

    default_value: float = 1.0

    def get_value(self) -> float:
        return self.canvas.zoom

    def set_value(self, value: float) -> None:
        self.canvas.zoom = value


class CanvasRotationController(CanvasBasedController):
    """
    Gives access to canvas rotation in degrees.

    - Operates on floats [0-360]
    - Defaults to 0.0
    """

    default_value: float = 0.0

    def get_value(self) -> float:
        return self.canvas.rotation

    def set_value(self, value: float) -> None:
        self.canvas.rotation = value
