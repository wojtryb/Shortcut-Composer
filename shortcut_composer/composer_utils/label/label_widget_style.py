# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import platform
from typing import Callable

from PyQt5.QtGui import QFont, QColor, QFontDatabase
from .label_text import LabelText


class LabelWidgetStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed callbacks.
    Can trim given text based on limits imposed by those callbacks.
    Creates font object with correct size based on amount of text.
    """

    def __init__(
        self,
        icon_radius_callback: Callable[[], int],
        border_thickness_callback: Callable[[], int],
        active_color_callback: Callable[[], QColor],
        background_color_callback: Callable[[], QColor],
        max_lines_amount_callback: Callable[[], int],
        max_signs_amount_callback: Callable[[], int],
    ) -> None:
        self._icon_radius_callback = icon_radius_callback
        self._border_thickness_callback = border_thickness_callback
        self._active_color_callback = active_color_callback
        self._background_color_callback = background_color_callback
        self._max_lines_amount_callback = max_lines_amount_callback
        self._max_signs_amount_callback = max_signs_amount_callback

    @property
    def icon_radius(self) -> int:
        return self._icon_radius_callback()

    @property
    def border_thickness(self) -> int:
        return self._border_thickness_callback()

    @property
    def active_color(self) -> QColor:
        return self._active_color_callback()

    @property
    def background_color(self) -> QColor:
        return self._background_color_callback()

    @property
    def active_color_dark(self) -> QColor:
        """Color variation of active element."""
        return QColor(
            round(self.active_color.red()*0.8),
            round(self.active_color.green()*0.8),
            round(self.active_color.blue()*0.8))

    @property
    def border_color(self) -> QColor:
        """Color of icon borders."""
        return QColor(
            min(self.background_color.red()+15, 255),
            min(self.background_color.green()+15, 255),
            min(self.background_color.blue()+15, 255))

    @property
    def max_lines_amount(self) -> int:
        return self._max_lines_amount_callback()

    @property
    def max_signs_amount(self) -> int:
        return self._max_signs_amount_callback()

    def trim_text(self, text: LabelText) -> list[str]:
        MAX_LINES = self.max_lines_amount
        MAX_SIGNS = self.max_signs_amount

        if not text.value:
            return []

        words = text.value.split("_")

        # Abbreviate words that are too long

        def abbreviate(word: str) -> str:
            if len(word) <= MAX_SIGNS:
                return word
            return word[:MAX_SIGNS-1] + "."
        words = list(map(abbreviate, words))

        # Merge short words into lines

        lines: list[str] = []
        last_line = words[0]
        longest_word = max(len(word) for word in words)

        for word in words[1:]:
            if len(last_line + word) < longest_word:
                last_line += " " + word
            else:
                lines.append(last_line)
                last_line = word

        if last_line:
            lines.append(last_line)

        # Remove lines at the end that do not fit into label

        if len(lines) > MAX_LINES:
            remainder = " ".join(lines[MAX_LINES:])
            last_line = lines[MAX_LINES-1] + " " + remainder
            lines[MAX_LINES-1] = last_line[:MAX_SIGNS-1].rstrip(' ') + "."

        return lines[:MAX_LINES]

    def get_font(self, widget_width: int, text_to_display: list[str]) -> QFont:
        """Return font to use in pyqt label."""
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setPointSize(round(
            self.SYSTEM_FONT_MULTIPLIER[platform.system()]
            * widget_width
            * self._content_size_multiplier(text_to_display)))
        font.setBold(True)
        return font

    def _content_size_multiplier(self, text_to_display: list[str]) -> float:
        amount_of_lines = len(text_to_display)
        longest_word = max(len(word) for word in text_to_display)

        return self.CONTENT_FONT_MULTIPLIER[amount_of_lines-1][longest_word-1]

    SYSTEM_FONT_MULTIPLIER = {
        "Linux": 0.175,
        "Windows": 0.11,
        "Darwin": 0.265,
        "": 0.125}
    """Font scale to apply on each OS."""

    CONTENT_FONT_MULTIPLIER: list[list[float]] = [
        [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4, 0.35],
        [0.9, 0.9, 0.81, 0.72, 0.63, 0.54, 0.45, 0.41, 0.36, 0.32],
        [0.6, 0.6, 0.54, 0.48, 0.42, 0.36, 0.3, 0.27, 0.24, 0.21]]
    """Font scale dependent on amount of lines and signs in each line."""
