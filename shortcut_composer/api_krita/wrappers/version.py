# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass
class Version:
    """
    Represents application version being compatible with semantic versioning.

    Allows to add optional info like git hash.
    Supports comparisons and parsing to string.
    """
    major: int
    minor: int
    fix: int
    additional_info: str = ""

    def __lt__(self, other: 'Version') -> bool:
        if isinstance(other, UnknownVersion):
            return True

        def version_as_int(version: Version) -> int:
            return version.major*1_000_000 + version.minor*1_000 + version.fix

        return version_as_int(self) < version_as_int(other)

    def __str__(self) -> str:
        if not self.additional_info:
            return f"{self.major}.{self.minor}.{self.fix}"
        return f"{self.major}.{self.minor}.{self.fix} {self.additional_info}"


class UnknownVersion(Version):
    """Represents unknown application version."""

    def __init__(self) -> None:
        super().__init__(0, 0, 0, "unknown")

    def __lt__(self, other: 'Version') -> bool:
        """Consider unknown version to be higher than any valid one."""
        return False

    def __str__(self) -> str:
        return "unknown"
