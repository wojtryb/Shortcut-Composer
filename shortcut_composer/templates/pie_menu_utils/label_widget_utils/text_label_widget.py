# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QFont,
    QColor,
    QFontDatabase,
    QPaintEvent,
)
from PyQt5.QtWidgets import QLabel, QWidget

from api_krita.pyqt import Painter, Text
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

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Paint the entire widget using the Painter wrapper.

        Paint a background behind a label and its border.
        """
        with Painter(self, event) as painter:
            painter.paint_wheel(
                center=self.center,
                outer_radius=self.icon_radius,
                color=self._style.icon_color)
            painter.paint_wheel(
                center=self.center,
                outer_radius=self.icon_radius,
                color=self._border_color,
                thickness=self._style.border_thickness)

    def _create_pyqt_label(self) -> QLabel:
        """Create and show a new Qt5 label. Does not need redrawing."""
        to_display = self.label.display_value

        if not isinstance(to_display, Text):
            raise TypeError("Label supposed to be text.")

        heigth = round(self.icon_radius*0.8)

        label = QLabel(self)
        label.setText(to_display.value)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, round(heigth*2), round(heigth))
        label.setFont(self._font)
        label.move(self.center.x()-heigth,
                   self.center.y()-heigth//2)
        label.setStyleSheet(f'''
            background-color:rgba({self._color_to_str(self._style.icon_color)});
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
