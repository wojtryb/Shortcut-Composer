# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from PyQt6.QtGui import *
except ImportError:
    from PyQt5.QtGui import *

    # Monkey patch for QDragMoveEvent adds compatibility with Qt6 syntax
    QDragMoveEvent.position = lambda self: self.posF()
