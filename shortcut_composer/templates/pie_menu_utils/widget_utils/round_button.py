from typing import Optional, Callable

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from ..pie_style import PieStyle
from ..pie_config import PieConfig
from api_krita.pyqt import BaseWidget


class RoundButton(QPushButton, BaseWidget):
    """
    Round button with a tick icon which uses provided PieStyle.

    `Radius callback` defines how the button radius is determined. Each
    change in passed `config` results in resetting the button size.
    """

    def __init__(
        self,
        icon: QIcon,
        icon_scale: float,
        radius_callback: Callable[[], int],
        style: PieStyle,
        config: PieConfig,
        parent: Optional[QWidget] = None,
    ):
        QPushButton.__init__(self, icon, "", parent)
        self.setCursor(Qt.ArrowCursor)

        self._radius_callback = radius_callback
        self._icon_scale = icon_scale
        self._style = style
        self._config = config
        self._config.register_callback(self._reset)

        if parent is None:
            self.setWindowFlags((
                self.windowFlags() |  # type: ignore
                Qt.Tool |
                Qt.FramelessWindowHint |
                Qt.NoDropShadowWindowHint))
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background: transparent;")

        self._reset()
        self.show()

    def _reset(self):
        """Reset the size and repaint the button."""
        radius = self._radius_callback()
        self.setGeometry(0, 0, radius*2, radius*2)

        self.setStyleSheet(f"""
            QPushButton [
                border: {self._style.border_thickness}px
                    {self._color_to_str(self._style.border_color)};
                border-radius: {radius}px;
                border-style: outset;
                background: {self._color_to_str(self._style.background_color)};
                qproperty-iconSize:{round(radius*self._icon_scale)}px;
            ]
            QPushButton:hover [
                background: {self._color_to_str(self._style.active_color)};
            ]
        """.replace('[', '{').replace(']', '}'))

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''rgba(
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()})'''
