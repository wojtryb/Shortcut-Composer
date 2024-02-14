# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import Config
from .rotation_painter import RotationPainter
from .rotation_config import RotationConfig

T = TypeVar('T')


class RotationWidget(AnimatedWidget, BaseWidget, Generic[T]):

    class Zone(Enum):
        DEADZONE = 0
        DISCRETE_ZONE = 1
        CONTIGUOUS_ZONE = 2

    def __init__(self, config: RotationConfig, parent=None) -> None:
        self._config = config

        self.selected_angle = 0
        self.selected_zone = self.Zone.DEADZONE

        AnimatedWidget.__init__(self, parent, Config.PIE_ANIMATION_TIME.read())

        self._config.register_callback(self._resize)
        self._resize()

        self.setAcceptDrops(True)
        self.setWindowFlags((
            self.windowFlags() |  # type: ignore
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.NoDropShadowWindowHint))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

    def reset_state(self):
        self.selected_angle = 0
        self.selected_zone = self.Zone.DEADZONE

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            RotationPainter(
                painter=painter,
                deadzone_radius=self._config.deadzone_radius,
                widget_radius=self._config.widget_radius)

    def _resize(self) -> None:
        self.setGeometry(0, 0, self._diameter, self._diameter)

    @property
    def _diameter(self):
        return self._config.widget_radius * 2
