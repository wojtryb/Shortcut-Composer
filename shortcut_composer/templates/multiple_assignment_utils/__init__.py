# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Widgets to display on the settings dialog."""

from .ma_settings_handler import MaSettingsHandler
from .ma_settings import MaSettings
from .ma_config import MaConfig

__all__ = [
    "MaSettingsHandler",
    "MaSettings",
    "MaConfig"]
