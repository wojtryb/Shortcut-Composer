# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum


class Zone(Enum):
    DEADZONE = 0
    DISCRETE_ZONE = 1
    CONTIGUOUS_ZONE = 2
