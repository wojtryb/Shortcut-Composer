# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Required part of api_krita package, so that no dependency is needed."""

from krita import Krita as Api
from typing import Any, Optional


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    def __init__(self) -> None:
        self.instance = Api.instance()

    def read_setting(
        self,
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> Optional[str]:
        """
        Read a setting from .kritarc file.

        - Return string red from file if present
        - Return default if it was given
        - Return None if default was not given
        """
        red_value = self.instance.readSetting(group, name, default)
        return None if red_value == "Not stored" else red_value

    def write_setting(self, group: str, name: str, value: Any) -> None:
        """Write setting to .kritarc file. Value type will be lost."""
        self.instance.writeSetting(group, name, str(value))


Krita = KritaInstance()
