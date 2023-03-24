# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, List, Union, Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QComboBox,
    QSpinBox,
    QWidget,
    QLabel)

from api_krita.wrappers import Database
from ..config.fields import ImmutableField


class FieldUiWrapper:
    def __init__(self, ui_widget: Union[QSpinBox, QDoubleSpinBox, QComboBox]):
        self.ui_widget = ui_widget

    def read(self):
        if isinstance(self.ui_widget, (QSpinBox, QDoubleSpinBox)):
            return self.ui_widget.value()
        return self.ui_widget.currentText()

    def write(self, value):
        if isinstance(self.ui_widget, (QSpinBox, QDoubleSpinBox)):
            return self.ui_widget.setValue(value)
        return self.ui_widget.setCurrentText(value)


class ConfigFormLayout(QFormLayout):
    """Dialog zone consisting of spin boxes."""

    def __init__(self, elements: List[Union[str, list, dict]]) -> None:
        super().__init__()
        self._forms: Dict[ImmutableField, FieldUiWrapper] = {}

        for element in elements:
            if isinstance(element, str):
                self._add_label(element)
            elif isinstance(element, list):
                self._add_row(*element)
            elif isinstance(element, dict):
                self._add_row(**element)
            else:
                raise TypeError("Unsupported arguments.")

    def _add_row(
            self,
            config: ImmutableField,
            step: Optional[float] = None,
            max_value: Optional[float] = None) -> None:
        field_ui = self.create_field_ui(config, step, max_value)
        self._forms[config] = field_ui
        self.addRow(config.name, field_ui.ui_widget)

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addRow(QSplitter(Qt.Horizontal))
        self.addRow(label)

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for config, form in self._forms.items():
            if config.type != str:
                form.write(config.read())  # type: ignore
            else:
                # HACK: can't assume the combobox is tag chooser
                with Database() as database:
                    combo_box = form.ui_widget
                    combo_box.clear()
                    combo_box.addItems(
                        sorted(database.get_brush_tags(), key=str.lower))
                    combo_box.setCurrentText(config.read())

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for config, form in self._forms.items():
            config.write(form.read())

    @staticmethod
    def create_field_ui(
        config: ImmutableField,
        step: Optional[float] = None,
        max_value: Optional[float] = None
    ):
        if config.type in (float, int):
            ui = QSpinBox() if config.type is int else QDoubleSpinBox()
            ui.setObjectName(config.name)
            ui.setMinimum(0)
            ui.setMaximum(max_value)  # type: ignore
            ui.setSingleStep(step)  # type: ignore
        elif config.type is str:
            ui = QComboBox()
            ui.setObjectName(config.name)
        else:
            raise TypeError(f"{config.type} not supported.")

        wrapper = FieldUiWrapper(ui)
        wrapper.write(config.read())
        return wrapper


class ConfigFormWidget(QWidget):
    def __init__(self, elements: List[Union[str, list, dict]]) -> None:
        super().__init__()

        self._layout = ConfigFormLayout(elements)
        stretched = QHBoxLayout()
        stretched.addStretch()
        stretched.addLayout(self._layout)
        stretched.addStretch()
        self.setLayout(stretched)

    def apply(self) -> None:
        self._layout.apply()

    def refresh(self) -> None:
        self._layout.refresh()
