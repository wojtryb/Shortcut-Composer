from typing import List

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QCursor

from api_krita.pyqt import AnimatedWidget, BaseWidget
from composer_utils.config import Config

from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import PieConfig


class PieSettings(AnimatedWidget, BaseWidget):
    def __init__(
        self,
        values: List[Label],
        style: PieStyle,
        pie_config: PieConfig,
        parent=None
    ) -> None:
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint))
        self.setCursor(Qt.ArrowCursor)

        self._values = values
        self._style = style
        self._pie_config = pie_config

    def move_to_pie_side(self):
        offset = self.width()//2 + self._style.widget_radius * 1.05
        point = QPoint(round(offset), 0)
        self.move_center(QCursor().pos() + point)  # type: ignore
