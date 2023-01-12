# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QComboBox,
    QWidget,
)

from api_krita.enums import BlendingMode, Tool
from ..utils import PieValues
from ..config import Config


class PieValuesTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.combo_widget_picker = QComboBox()
        self.widgets = {
            "Blending modes": PieValues(
                allowed_values=set(BlendingMode._member_names_),
                config=Config.BLENDING_MODES_VALUES
            ),
            "Selection tools": PieValues(
                allowed_values=set(Tool._member_names_),
                config=Config.SELECTION_TOOLS_VALUES
            ),
            "Misc tools": PieValues(
                allowed_values=set(Tool._member_names_),
                config=Config.MISC_TOOLS_VALUES
            ),
            "Transform modes": PieValues(
                allowed_values=set(Tool._member_names_),
                config=Config.TRANSFORM_MODES_VALUES
            ),
        }
        self.combo_widget_picker.addItems(self.widgets.keys())
        self.combo_widget_picker.currentTextChanged.connect(
            self._change_widget)

        layout.addWidget(self.combo_widget_picker)
        for widget in self.widgets.values():
            widget.hide()
            layout.addWidget(widget)
        self.widgets["Blending modes"].show()
        self.setLayout(layout)

    def _change_widget(self):
        for widget in self.widgets.values():
            widget.hide()
        self.widgets[self.combo_widget_picker.currentText()].show()

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        for widget in self.widgets.values():
            widget.apply()

    def refresh(self) -> None:
        """Ask all dialog zones to refresh themselves."""
        for widget in self.widgets.values():
            widget.refresh()
