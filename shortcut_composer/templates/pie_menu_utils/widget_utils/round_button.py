from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from ..pie_style import PieStyle
from api_krita.pyqt import BaseWidget


class RoundButton(QPushButton, BaseWidget):
    """Round button with a tick icon which uses provided PieStyle."""

    def __init__(
        self,
        radius: int,
        icon_scale: float,
        style: PieStyle,
        icon: QIcon,
        parent: Optional[QWidget] = None
    ):
        QPushButton.__init__(self, icon, "", parent)
        self.setGeometry(0, 0, radius*2, radius*2)
        self.setCursor(Qt.ArrowCursor)
        self.setStyleSheet(f"""
            QPushButton [
                border: {style.border_thickness}px
                    {self._color_to_str(style.border_color)};
                border-radius: {radius}px;
                border-style: outset;
                background: {self._color_to_str(style.background_color)};
                qproperty-iconSize:{round(radius*icon_scale)}px;
            ]
            QPushButton:hover [
                background: {self._color_to_str(style.active_color)};
            ]
        """.replace('[', '{').replace(']', '}'))

        if parent is None:
            self.setWindowFlags((
                self.windowFlags() |  # type: ignore
                Qt.Tool |
                Qt.FramelessWindowHint |
                Qt.NoDropShadowWindowHint))
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background: transparent;")

        self.show()

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''rgba(
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()})'''
