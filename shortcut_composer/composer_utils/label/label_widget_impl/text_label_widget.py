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

        label = QLabel(self)
        label.setText(to_display.value)
        label.setAlignment(Qt.AlignCenter)
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
        font = QFontDatabase.systemFont(QFontDatabase.TitleFont)
        font.setPointSize(round(
            self._label_widget_style.font_multiplier
            * self.width()
            * self._sign_amount_multiplier))
        font.setBold(True)
        return font

    @property
    def _sign_amount_multiplier(self) -> float:
        """Return multiplier (0-1) getting smaller the more signs are there."""
        to_display = self.label.display_value

        if not isinstance(to_display, LabelText):
            raise TypeError("Label supposed to be text.")

        signs_amount = len(to_display.value)
        if signs_amount <= 4:
            return 1
        return 4/(signs_amount)

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''
