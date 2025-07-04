# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, field

try:
    from PyQt5.QtGui import QColor
except ModuleNotFoundError:
    from PyQt6.QtGui import QColor


@dataclass
class LabelText:
    """Text along with its color."""

    value: str
    color: QColor = field(default_factory=lambda: QColor("white"))
