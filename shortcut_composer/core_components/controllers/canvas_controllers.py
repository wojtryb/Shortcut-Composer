from api_krita import Krita
from ..controller_base import Controller


class CanvasZoomController(Controller):
    """
    Gives access to zoom.

    - Operates on floats
    - Defaults to 1.0
    """

    default_value: int = 1.0

    @staticmethod
    def get_value() -> float:
        return Krita.get_active_canvas().zoom()

    @staticmethod
    def set_value(value: float) -> None:
        Krita.get_active_canvas().set_zoom(value)


class CanvasRotationController(Controller):
    """
    Gives access to canvas rotation in degrees.

    - Operates on floats [0-360]
    - Defaults to 0.0
    """

    default_value: int = 0.0

    @staticmethod
    def get_value() -> float:
        return Krita.get_active_canvas().rotation()

    @staticmethod
    def set_value(value: float) -> None:
        Krita.get_active_canvas().set_rotation(value)
