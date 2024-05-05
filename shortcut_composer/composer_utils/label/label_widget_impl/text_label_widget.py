# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QFontDatabase
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita import Krita
from ..label_text import LabelText
from ..label_widget import LabelWidget
from ..label_interface import LabelInterface
from ..label_widget_style import LabelWidgetStyle

T = TypeVar("T", bound=LabelInterface)

MAX_LINES = 2
MAX_SIGNS = 8

class TextLabelWidget(LabelWidget[T]):
    """Displays a `label` which holds text."""

    def __init__(
        self,
        label: T,
        label_widget_style: LabelWidgetStyle,
        parent: QWidget,
    ) -> None:
        super().__init__(label, label_widget_style, parent)

        self._display_value = self._get_display_value()
        self._pyqt_label = self._create_pyqt_label()

    def _get_display_value(self) -> list[str]:
        to_display = self.label.display_value

        if not isinstance(to_display, LabelText):
            raise TypeError("Label supposed to be text.")

        words = to_display.value.split("_")
        if not words:
            return []

        changed_words = []
        for word in words:
            if len(word) <= MAX_SIGNS:
                changed_words.append(word)
            else:
                changed_words.append(word[:MAX_SIGNS-1]+".")
        words = changed_words

        longest_word = max(len(word) for word in words)

        output = []
        last_line = words[0]

        for word in words[1:]:
            if len(last_line + " " + word) <= longest_word:
                last_line += " " + word
            else:
                output.append(last_line)
                last_line = word

        if last_line:
            output.append(last_line)

        if len(output) > MAX_LINES:
            remainder = " ".join(output[MAX_LINES:])
            output[MAX_LINES-1] += " " + remainder
            output[MAX_LINES-1] = output[MAX_LINES-1][:MAX_SIGNS-1] + "."

        return output[:MAX_LINES]

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, LabelText):
            raise TypeError("Label supposed to be text.")

        height = round(self.icon_radius*0.75)

        label = QLabel(self)
        label.setText(to_display.value)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.resize(round(height*2), round(height))
        label.setFont(self._font)
        label.move(self.center.x()-height,
                   self.center.y()-height//2)
        label.setStyleSheet(f'''
            background-color:rgba({self._color_to_str(
            Krita.get_main_color_from_theme())});
            color:rgba({self._color_to_str(to_display.color)});
        ''')

        label.show()
        return label

    @property
    def _font(self) -> QFont:
        """Return font to use in pyqt label."""
        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.TitleFont)
        font.setPointSize(round(
            self._label_widget_style.font_multiplier
            * self.width()
            * self._content_size_multiplier))
        font.setBold(True)
        return font

    @property
    def _content_size_multiplier(self) -> float:
        line_amount_multiplier = {
            1: 1.0,
            2: 0.9,
            3: 0.6,
        }[len(self._display_value)]

        longest_word = max(len(word) for word in self._display_value)
        sign_amount_multiplier = {
            1: 1.0,
            2: 1.0,
            3: 0.9,
            4: 0.8,
            5: 0.7,
            6: 0.6,
            7: 0.5,
            8: 0.45,
            9: 0.4,
            10: 0.35,
        }[longest_word]

        return line_amount_multiplier * sign_amount_multiplier

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''
