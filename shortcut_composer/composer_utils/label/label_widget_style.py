# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from typing import Callable

from PyQt5.QtGui import QFont, QColor, QFontDatabase

from composer_utils import Config


class LabelWidgetStyle:
    """
    Holds and calculates configuration of displayed elements.

    Style elements are calculated based on passed callbacks.
    Can split given text based on limits imposed by those callbacks.
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
        abbreviation_sign_callback: Callable[[], str],
    ) -> None:
        self._icon_radius_callback = icon_radius_callback
        self._border_thickness_callback = border_thickness_callback
        self._active_color_callback = active_color_callback
        self._background_color_callback = background_color_callback
        self._max_lines_amount_callback = max_lines_amount_callback
        self._max_signs_amount_callback = max_signs_amount_callback
        self._abbreviation_sign_callback = abbreviation_sign_callback

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

    def split_text_to_lines(self, text: str) -> list[str]:
        """
        Split the text into lines, according to limits from this class.

        On initialization, this object received callbacks parametrizing
        the split:
        - maximal amount of lines the text can consist of
        - maximal amount of signs in every line of text
        - sign to mark that the word or line got abbreviated

        Passed string is split to words on whitespaces and underscores.
        If the word is too long to fit in single line it gets shortened.
        Then those words are getting concatenated.
        If a line gets too long, next word is placed in the next line.
        After the line limit is met, the rest of text gets discarded.

        Abbreviation sign is not counted towards signs limit.

        Example usage: (3 lines, 8 signs, '.' as abbreviation sign):
        Input: 'This is inscription with text that is too long'
        Output ['This is', 'inscript.' 'with text.']
        """
        MAX_LINES = self._max_lines_amount_callback()
        MAX_SIGNS = self._max_signs_amount_callback()
        ABBR_SIGN = self._abbreviation_sign_callback()

        if not text:
            return []

        words = re.split(r"\W+|_", text)

        # Abbreviate words that are too long

        def abbreviate(word: str) -> str:
            if len(word) <= MAX_SIGNS:
                return word
            return word[:MAX_SIGNS] + ABBR_SIGN
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
            lines[MAX_LINES-1] = last_line[:MAX_SIGNS].rstrip(' ') + ABBR_SIGN

        return lines[:MAX_LINES]

    def get_font(self, widget_width: int, text_to_display: list[str]) -> QFont:
        """Return font to use in pyqt label."""
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setPointSize(round(
            0.175
            * widget_width
            * Config.TEXT_LABEL_GLOBAL_SCALE.read()
            * self._content_size_multiplier(text_to_display)))
        font.setBold(True)
        return font

    def _content_size_multiplier(self, text_to_display: list[str]) -> float:
        """Return text scale based on amount of signs in the longest line."""
        longest_word = max(len(word) for word in text_to_display)
        return self.CONTENT_FONT_MULTIPLIER[longest_word-1]

    CONTENT_FONT_MULTIPLIER: list[float] = [
        1, 1, 1, 0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.4]
    """Font scale dependent on amount of signs in the longest line."""
