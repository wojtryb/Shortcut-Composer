# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Callable

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from api_krita.pyqt import RoundButton
from .pie_style import PieStyle
from .pie_config import PieConfig


class PieButton(RoundButton):
    """
    Round button with custom icon, which uses provided PieStyle.

    `radius_callback` defines how the button radius is determined. Each
    change in passed `config` results in resetting the button size.
    """

    def __init__(
        self,
        icon: QIcon,
        icon_scale: float,
        radius_callback: Callable[[], int],
        pie_style: PieStyle,
        config: PieConfig,
        parent: Optional[QWidget] = None,
    ) -> None:
        self._radius_callback = radius_callback
        self._pie_style = pie_style
        config.register_callback(self.refresh)

        super().__init__(
            icon=icon,
            icon_scale=icon_scale,
            initial_radius=radius_callback(),
            background_color=pie_style.background_color,
            active_color=pie_style.active_color,
            parent=parent)

    def refresh(self) -> None:
        self._radius = self._radius_callback()
        self._background_color = self._pie_style.background_color
        self._active_color = self._pie_style.active_color
        super().refresh()
