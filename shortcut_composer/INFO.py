# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Importable information about the plugin."""

from api_krita.wrappers import Version

__version__ = Version(1, 5, 4)
"""Version of the Shortcut Composer plugin."""

__required_krita_version__ = Version(5, 2, 2)
"""Version of krita required by the plugin to work."""

__author__ = "Wojciech Trybus"
"""Maintainer of the plugin."""

__license__ = "GPL-3.0-or-later"
"""Plugin license."""
