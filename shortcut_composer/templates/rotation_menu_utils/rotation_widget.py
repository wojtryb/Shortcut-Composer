# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import Config
from .rotation_style_holder import RotationStyleHolder
from .rotation_painter import RotationPainter
from .rotation_config import RotationConfig
from .zone import Zone

T = TypeVar('T')


class RotationWidget(AnimatedWidget, BaseWidget, Generic[T]):

    def __init__(
        self,
        config: RotationConfig,
        style_holder: RotationStyleHolder,
        parent=None
    ) -> None:
        self._config = config
        self._style_holder = style_holder

        self.selected_angle = 0
        self.selected_zone = Zone.DEADZONE

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

        self._rotation_painter = RotationPainter(
            style=self._style_holder.rotation_style)

    def reset_state(self):
        self.selected_angle = 0
        self.selected_zone = Zone.DEADZONE

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            self._rotation_painter.paint(
                painter=painter,
                selected_angle=self.selected_angle,
                selected_zone=self.selected_zone)

    def _resize(self) -> None:
        self.setGeometry(0, 0, self._diameter, self._diameter)

    @property
    def _diameter(self):
        diameter = self._config.widget_radius * 2
        # make sure there is a place for settings button
        return max(diameter, self._config.settings_button_radius*2)
