from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QPainter,
    QPixmap,
    QImage,
    QBrush,
    QWindow
)

from api_krita import Krita
from api_krita.enums import BlendingMode
from ..controller_base import Controller


class ViewBasedController(Controller):
    """Family of controllers which operate on values from active view."""

    def refresh(self):
        """Refresh currently stored active view."""
        self.view = Krita.get_active_view()


class PresetController(ViewBasedController):
    """
    Gives access to `presets`.

    - Operates on `string` representing name of preset
    - Does not have a default

    Example preset name: `"b) Basic-5 Size Opacity"`
    """

    def get_value(self) -> str:
        """Get currently active preset."""
        return self.view.brush_preset

    def set_value(self, value: str) -> None:
        """Set a preset of passed name."""
        self.view.brush_preset = value

    def get_label(self, value: str) -> QPixmap:
        image = Krita.get_presets()[value].image()
        return self._mask_image(image, size=100)

    @staticmethod
    def _mask_image(image: QImage, size=100) -> QPixmap:
        image.convertToFormat(QImage.Format_ARGB32)

        imgsize = min(image.width(), image.height())
        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        brush = QBrush(image)
        painter = QPainter(out_img)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawEllipse(0, 0, imgsize, imgsize)
        painter.end()

        pixel_ratio = QWindow().devicePixelRatio()
        pixmap = QPixmap.fromImage(out_img)
        pixmap.setDevicePixelRatio(pixel_ratio)
        new_size = round(size * pixel_ratio)
        pixmap = pixmap.scaled(
            new_size,
            new_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        return pixmap


class BrushSizeController(ViewBasedController):
    """
    Gives access to `brush size`.

    - Operates on `float` representing brush size in pixels
    - Defaults to `100`
    """

    default_value: float = 100

    def get_value(self) -> float:
        return self.view.brush_size

    def set_value(self, value: float) -> None:
        self.view.brush_size = value

    def get_label(self, value: float) -> str:
        return f"{round(value)}px"


class BlendingModeController(ViewBasedController):
    """
    Gives access to `brush blending mode`.

    - Operates on `BlendingMode`
    - Defaults to `BlendingMode.NORMAL`
    """

    default_value = BlendingMode.NORMAL

    def get_value(self) -> BlendingMode:
        """Get currently active blending mode."""
        return self.view.blending_mode

    def set_value(self, value: BlendingMode) -> None:
        """Set a passed blending mode."""
        self.view.blending_mode = value

    def get_label(self, value: BlendingMode) -> str:
        return value.name[0]


class OpacityController(ViewBasedController):
    """
    Gives access to `brush opacity` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        """Get current brush opacity."""
        return self.view.opacity

    def set_value(self, value: int) -> None:
        """Set passed brush opacity."""
        self.view.opacity = value

    def get_label(self, value: int) -> str:
        return f"{value}%"


class FlowController(ViewBasedController):
    """
    Gives access to `brush flow` in %.

    - Operates on `integer` in range `0 to 100`
    - Defaults to `100`
    """

    default_value: int = 100

    def get_value(self) -> int:
        return self.view.flow

    def set_value(self, value: int) -> None:
        self.view.flow = value

    def get_label(self, value: int) -> str:
        return f"{value}%"
