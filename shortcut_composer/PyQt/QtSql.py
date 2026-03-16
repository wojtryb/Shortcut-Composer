# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from PyQt6.QtSql import *
except ImportError:
    from PyQt5.QtSql import *
