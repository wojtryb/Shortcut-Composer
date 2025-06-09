# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar, Protocol

from PyQt5.QtGui import QPixmap, QIcon, QColor

from .label_text import LabelText

T = TypeVar("T")


class LabelInterface(Protocol, Generic[T]):
    """
    Data of any type with its graphical and string representation.

    - `value` -- Value to set using the controller
    - `display_value` -- `value` representation to display.
                         Multiple types are supported.
    - `pretty_name` -- String to use when displaying the label to user
    """

    value: T
    display_value: QPixmap | QIcon | LabelText | QColor | None
    pretty_name: str
