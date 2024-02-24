# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Components used by the core of the config system."""

from .api_krita import Krita
from .save_location import SaveLocation

__all__ = ["Krita", "SaveLocation"]
