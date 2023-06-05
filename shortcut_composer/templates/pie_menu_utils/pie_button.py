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
        style: PieStyle,
        config: PieConfig,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(
            icon=icon,
            icon_scale=icon_scale,
            initial_radius=radius_callback(),
            background_color=style.background_color,
            active_color=style.active_color,
            parent=parent)

        config.register_callback(lambda: self.resize(radius_callback()))
