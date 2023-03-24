# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api
from typing import Any


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    def __init__(self) -> None:
        self.instance = Api.instance()

    def read_setting(self, group: str, name: str, default: str) -> str:
        """Read setting from .kritarc file as string."""
        return self.instance.readSetting(group, name, default)

    def write_setting(self, group: str, name: str, value: Any) -> None:
        """Write setting to .kritarc file. Value type will be lost."""
        self.instance.writeSetting(group, name, str(value))


Krita = KritaInstance()
