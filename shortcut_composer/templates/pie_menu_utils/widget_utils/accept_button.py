from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from ..pie_style import PieStyle
from api_krita.pyqt import BaseWidget
from api_krita import Krita


class AcceptButton(QPushButton, BaseWidget):
    """Round button with a tick icon which uses provided PieStyle."""

    def __init__(self, style: PieStyle, parent: Optional[QWidget] = None):
        QPushButton.__init__(self, Krita.get_icon("dialog-ok"), "", parent)
        if parent is None:
            self.setWindowFlags((
                self.windowFlags() |  # type: ignore
                Qt.Tool |
                Qt.FramelessWindowHint |
                Qt.NoDropShadowWindowHint))
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background: transparent;")

        self._style = style
        self.hide()
        if self._style.deadzone_radius != float("inf"):
            self.radius = int(self._style.deadzone_radius)
        else:
            self.radius = 1
        self.setCursor(Qt.ArrowCursor)
        self.setGeometry(
            0, 0,
            self.radius*2,
            self.radius*2)

        self.setStyleSheet(f"""
            QPushButton [
                border: {self._style.border_thickness}px
                    {self._color_to_str(self._style.border_color)};
                border-radius: {self.radius}px;
                border-style: outset;
                background: {self._color_to_str(self._style.background_color)};
                qproperty-iconSize:{round(self.radius*1.5)}px;
            ]
            QPushButton:hover [
                background: {self._color_to_str(self._style.active_color)};
            ]
        """.replace('[', '{').replace(']', '}')
        )
        self.show()

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''rgba(
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()})'''
