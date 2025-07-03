# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar

from PyQt5.QtGui import QPixmap, QIcon

from composer_utils.label import LabelText

T = TypeVar("T")


class Controller(Generic[T]):
    """Component that allows to get and set a specific property of krita."""

    TYPE: type[T]
    REQUIRES_TEXT_SETTINGS: bool = False
    DEFAULT_VALUE: T | None = None

    def refresh(self) -> None:
        """Refresh stored krita components."""
        ...

    def get_value(self) -> T:
        """Get handled value from krita."""
        ...

    def set_value(self, value: T) -> None:
        """Set handled value in krita."""
        ...

    def get_label(self, value: T) -> LabelText | QPixmap | QIcon | None:
        """Get value representation that can be displayed in GUI,"""
        ...

    def get_pretty_name(self, value: T) -> str:
        """Get value name that can be displayed to the user in GUI."""
        return str(value)


class NumericController(Controller[int]):
    TYPE = int
    REQUIRES_TEXT_SETTINGS: bool = False

    DEFAULT_VALUE: int
    MIN_VALUE: int
    MAX_VALUE: int

    STEP: int
    WRAPPING: bool
    ADAPTIVE: bool
