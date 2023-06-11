# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from .custom_widgets import BaseWidget


class RoundButton(QPushButton, BaseWidget):
    """Round button with custom icon."""

    def __init__(
        self, *,
        icon: QIcon = QIcon(),
        icon_scale: float = 1,
        initial_radius: int,
        background_color: QColor,
        active_color: QColor,
        parent: Optional[QWidget] = None,
    ) -> None:
        QPushButton.__init__(self, icon, "", parent)
        self.setCursor(Qt.ArrowCursor)

        self._icon_scale = icon_scale
        self._background_color = background_color
        self._active_color = active_color

        if parent is None:
            self.setWindowFlags((
                self.windowFlags() |  # type: ignore
                Qt.Tool |
                Qt.FramelessWindowHint |
                Qt.NoDropShadowWindowHint))
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setStyleSheet("background: transparent;")

        self.resize(initial_radius)
        self.show()

    def resize(self, radius: int) -> None:
        """Change the size and repaint the button."""
        self.setGeometry(0, 0, radius*2, radius*2)

        self.setStyleSheet(f"""
            QPushButton [
                border: {round(radius*0.06)}px
                    {self._color_to_str(self._border_color)};
                border-radius: {radius}px;
                border-style: outset;
                background: {self._color_to_str(self._background_color)};
                qproperty-iconSize:{round(radius*self._icon_scale)}px;
            ]
            QPushButton:hover [
                background: {self._color_to_str(self._active_color)};
            ]
        """.replace('[', '{').replace(']', '}'))

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''rgba(
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()})'''

    @property
    def _border_color(self) -> QColor:
        """Color of button border."""
        return QColor(
            min(self._background_color.red()+15, 255),
            min(self._background_color.green()+15, 255),
            min(self._background_color.blue()+15, 255),
            255)
