# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type, TypeVar

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
)
from ...text import Text
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface
from .icon_label_widget import IconLabelWidget
from .text_label_widget import TextLabelWidget
from .image_label_widget import ImageLabelWidget

T = TypeVar("T", bound=LabelInterface)


def dispatch_label_widget(label: T) -> Type[LabelWidget[T]]:
    """Return type of LabelWidget proper for given label."""
    if label.display_value is None:
        raise ValueError(f"Label {label} is not valid")

    return {
        QPixmap: ImageLabelWidget,
        Text: TextLabelWidget,
        QIcon: IconLabelWidget,
    }[type(label.display_value)]
