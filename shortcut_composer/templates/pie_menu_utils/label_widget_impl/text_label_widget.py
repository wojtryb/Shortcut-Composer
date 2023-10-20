# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QFontDatabase
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita import Krita
from api_krita.pyqt import Text
from ..pie_style import PieStyle
from ..label import Label
from ..label_widget import LabelWidget


class TextLabelWidget(LabelWidget):
    """Displays a `label` which holds text."""

    def __init__(
        self,
        label: Label,
        style: PieStyle,
        parent: QWidget,
        is_unscaled: bool = False,
    ) -> None:
        super().__init__(label, style, parent, is_unscaled)
        self._pyqt_label = self._create_pyqt_label()

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, Text):
            raise TypeError("Label supposed to be text.")

        height = round(self.icon_radius*0.8)

        label = QLabel(self)
        label.setText(to_display.value)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, round(height*2), round(height))
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
        font.setPointSize(round(self._style.font_multiplier*self.width()))
        font.setBold(True)
        return font

    @staticmethod
    def _color_to_str(color: QColor) -> str: return f'''
        {color.red()}, {color.green()}, {color.blue()}, {color.alpha()}'''
