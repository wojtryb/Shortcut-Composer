# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPaintEvent

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import Config
from .rotation_style import RotationStyle
from .rotation_widget_state import WidgetState
from .rotation_painter import RotationPainter
from .rotation_config import RotationConfig

T = TypeVar('T')


class RotationWidget(AnimatedWidget, BaseWidget, Generic[T]):

    def __init__(
        self,
        config: RotationConfig,
        style: RotationStyle,
        parent=None
    ) -> None:
        self._config = config
        self._style = style

        self.state = WidgetState()

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

        self._rotation_painter = RotationPainter(style=self._style)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as painter:
            self._rotation_painter.paint(
                painter=painter,
                state=self.state)

    def _resize(self) -> None:
        self.setGeometry(0, 0, self._diameter, self._diameter)

    @property
    def _diameter(self):
        diameter = self._style.widget_radius * 2
        # make sure there is a place for settings button
        return max(diameter, self._style.settings_button_radius*2)
