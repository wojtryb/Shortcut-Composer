from api_krita import Krita
from ..controller_base import Controller


class CanvasBasedController(Controller):
    """
    Family of controllers which operate on values from active document.

    As canvas operates on OpenGL, those controllers cannot be used in
    threads other than GUI, as they cause Krita to crash (5.0.6).
    """

    def refresh(self):
        """Refresh currently stored canvas."""
        self.canvas = Krita.get_active_canvas()


class CanvasZoomController(CanvasBasedController):
    """
    Gives access to `zoom`.

    - Operates on `float`
    - Defaults to `1.0`
    """

    default_value: float = 100.0

    def get_value(self) -> float:
        return self.canvas.zoom

    def set_value(self, value: float) -> None:
        self.canvas.zoom = value


class CanvasRotationController(CanvasBasedController):
    """
    Gives access to `canvas rotation` in degrees.

    - Operates on `float` in range `0.0 to 360.0`
    - Other values are expressed in that range
    - Defaults to `0.0`
    """

    default_value: float = 0.0

    def get_value(self) -> float:
        return self.canvas.rotation

    def set_value(self, value: float) -> None:
        self.canvas.rotation = value
