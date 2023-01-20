# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QComboBox,
    QWidget,
)

from api_krita.enums import BlendingMode, Tool, TransformMode
from ..utils import ActionValues
from ..config import Config


class ActionValuesTab(QWidget):
    """Tab in which user can change values used in actions and their order."""

    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.combo_widget_picker = QComboBox()
        self.widgets = {
            "Blending modes": ActionValues(
                allowed_values=set(BlendingMode._member_names_),
                config=Config.BLENDING_MODES_VALUES
            ),
            "Create layer with blending": ActionValues(
                allowed_values=set(BlendingMode._member_names_),
                config=Config.CREATE_BLENDING_LAYER_VALUES
            ),
            "Selection tools": ActionValues(
                allowed_values=set(Tool._member_names_),
                config=Config.SELECTION_TOOLS_VALUES
            ),
            "Misc tools": ActionValues(
                allowed_values=set(Tool._member_names_),
                config=Config.MISC_TOOLS_VALUES
            ),
            "Transform modes": ActionValues(
                allowed_values=set(TransformMode._member_names_),
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
        """Show a selectable list for a different action."""
        for widget in self.widgets.values():
            widget.hide()
        self.widgets[self.combo_widget_picker.currentText()].show()

    def apply(self) -> None:
        """Save values and their order for each selectable list."""
        for widget in self.widgets.values():
            widget.apply()

    def refresh(self) -> None:
        """Refresh each selectable list by loading values from settings."""
        for widget in self.widgets.values():
            widget.refresh()
