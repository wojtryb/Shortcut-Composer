# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita import Krita
from ..label_text import LabelText
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface
from ..label_widget_style import LabelWidgetStyle

T = TypeVar("T", bound=LabelInterface)


class TextLabelWidget(LabelWidget[T]):
    """Displays a `label` which holds text."""

    def __init__(
        self,
        label: T,
        label_widget_style: LabelWidgetStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(label, label_widget_style, parent)
        self._pyqt_label = self._create_pyqt_label()

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, LabelText):
            raise TypeError("Label supposed to be text.")

        height = round(self.icon_radius*0.75)
        trimmed_text = self._label_widget_style.trim_text(to_display)

        label = QLabel(self)
        label.setText("\n".join(trimmed_text))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.resize(height*2, height)
        font = self._label_widget_style.get_font(height*2, trimmed_text)
        label.setFont(font)
        label.move(self.center.x()-height,
                   self.center.y()-height//2)
        label.setStyleSheet(f'''
            background-color:rgba({
                self._color_to_str(Krita.get_main_color_from_theme())});
            color:rgba({self._color_to_str(to_display.color)});
        ''')

        label.show()
        return label

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''
