# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from PyQt5.QtGui import QColor


@dataclass
class Text:
    """Text along with its color."""

    value: str
    color: QColor = QColor("white")
