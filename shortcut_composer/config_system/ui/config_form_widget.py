# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFormLayout,
    QSplitter,
    QWidget,
    QLabel)

from .config_based_widget import ConfigBasedWidget


class ConfigFormWidget(QWidget):
    """
    Configuration Widget with a form of ConfigBasedWidgets.

    Consists of centered titles and labelled widgets added with
    `add_row()` and `add_title`.

    Alternatively, it can be initialized with a list of strings and
    ConfigBasedWidgets which create titles and form rows.

    Synchronizes stored ConfigBasedWidgets by allowing to refresh and
    save values to config of all stored ones.
    """

    def __init__(self, elements: list[ConfigBasedWidget | str]) -> None:
        super().__init__()
        self._layout = QFormLayout()
        self._layout.RowWrapPolicy(QFormLayout.DontWrapRows)
        self._layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self._layout.setLabelAlignment(Qt.AlignRight)
        self._layout.setFormAlignment(
            Qt.AlignHCenter | Qt.AlignTop)  # type: ignore
        self.setLayout(self._layout)

        self.widgets: list[ConfigBasedWidget] = []
        for element in elements:
            if isinstance(element, str):
                self.add_title(element)
            elif isinstance(element, ConfigBasedWidget):
                self.add_row(element)
            else:
                raise TypeError("Unsupported arguments.")

    def add_row(self, element: ConfigBasedWidget) -> None:
        """Add a ConfigBasedWidget along with a label."""
        self.widgets.append(element)
        self._layout.addRow(f"{element.pretty_name}:", element.widget)

    def add_title(self, text: str) -> None:
        """Add a label with given text."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold")
        self._layout.addRow(QSplitter(Qt.Horizontal))
        self._layout.addRow(label)

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for element in self.widgets:
            element.reset()

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for element in self.widgets:
            element.save()
