# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Union, Generic, TypeVar, Protocol

from PyQt5.QtGui import QPixmap, QIcon

from ..text import Text

T = TypeVar("T")


class LabelInterface(Protocol, Generic[T]):
    """
    Data of any type with its graphical and string representation.

    - `value` -- Value to set using the controller
    - `display_value` -- `value` representation to display. Can be
                         either a colored text or an image
    - `pretty_name` -- String to use when displaying the label to user
    """

    value: T
    display_value: Union[QPixmap, QIcon, Text, None]
    pretty_name: str
