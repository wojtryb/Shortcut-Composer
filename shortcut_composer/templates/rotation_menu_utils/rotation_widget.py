# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QPaintEvent)

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import Config
from .rotation_painter import RotationPainter
from .rotation_config import RotationConfig

T = TypeVar('T')


class RotationWidget(AnimatedWidget, BaseWidget, Generic[T]):

    def __init__(self, config: RotationConfig, parent=None) -> None:
        self._config = config
        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())
        diameter = self._radius * 2
        self.setGeometry(0, 0, diameter, diameter)

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            RotationPainter(painter, self._radius)

    @property
    def _radius(self):
        return round(self._config.DEADZONE_SCALE.read() * 100)
