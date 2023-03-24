# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QSplitter,
    QWidget,
    QLabel)

from .config_based_widget import ConfigBasedWidget


class ConfigFormWidget(QWidget):
    """Dialog zone consisting of spin boxes."""

    def __init__(self, elements: List[Union[ConfigBasedWidget, str]]) -> None:
        super().__init__()
        self._layout = QFormLayout()
        self._layout.RowWrapPolicy(QFormLayout.DontWrapRows)
        self._layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self._layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self._layout.setLabelAlignment(Qt.AlignRight)
        self.setLayout(self._layout)

        self._widgets: List[ConfigBasedWidget] = []
        for element in elements:
            if isinstance(element, str):
                self._add_label(element)
            elif isinstance(element, ConfigBasedWidget):
                self._add_row(element)
            else:
                raise TypeError("Unsupported arguments.")

    def _add_row(self, element: ConfigBasedWidget) -> None:
        self._widgets.append(element)
        self._layout.addRow(f"{element.pretty_name}:", element.widget)

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self._layout.addRow(QSplitter(Qt.Horizontal))
        self._layout.addRow(label)

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for element in self._widgets:
            element.reset()

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for element in self._widgets:
            element.save()
