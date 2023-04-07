# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Type

from PyQt5.QtGui import (
    QPixmap,
    QIcon,
)
from PyQt5.QtWidgets import QWidget

from api_krita.pyqt import Text
from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget
from .icon_label_widget import IconLabelWidget
from .text_label_widget import TextLabelWidget
from .image_label_widget import ImageLabelWidget


def create_label_widget(
    label: Label,
    style: PieStyle,
    parent: QWidget,
    is_unscaled: bool = False,
) -> 'LabelWidget':
    """Return LabelWidget which can display this label."""
    if label.display_value is None:
        raise ValueError(f"Label {label} is not valid")

    painter_type: Type[LabelWidget] = {
        QPixmap: ImageLabelWidget,
        Text: TextLabelWidget,
        QIcon: IconLabelWidget,
    }[type(label.display_value)]

    return painter_type(label, style, parent, is_unscaled)
