# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import abstractmethod
from typing import Any, List, Union, Final, Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QSplitter,
    QComboBox,
    QSpinBox,
    QWidget,
    QLabel)

from ..config import ImmutableField


class ConfigBasedWidget:
    def __init__(
        self,
        config_field: ImmutableField,
        parent: Optional[QWidget] = None
    ) -> None:
        self._parent = parent
        self.config_field: Final[ImmutableField] = config_field
        self.widget: QWidget

    @abstractmethod
    def read(self): ...

    @abstractmethod
    def set(self, value): ...

    def reset(self):
        self.set(self.config_field.read())

    def save(self):
        self.config_field.write(self.read())


class ConfigSpinBox(ConfigBasedWidget):
    def __init__(
        self,
        config_field: Union[ImmutableField[int], ImmutableField[float]],
        parent: Optional[QWidget] = None,
        step: float = 1,
        max_value: float = 100,
    ) -> None:
        super().__init__(config_field, parent)
        self._step = step
        self._max_value = max_value
        self._spin_box = self._init_spin_box()
        self.widget: Final[Union[QSpinBox, QDoubleSpinBox]] = self._spin_box
        self.reset()

    def read(self):
        return self._spin_box.value()

    def set(self, value):
        self._spin_box.setValue(value)

    def _init_spin_box(self):
        spin_box = (QSpinBox() if self.config_field.type is int
                    else QDoubleSpinBox())
        spin_box.setObjectName(self.config_field.name)
        spin_box.setMinimum(0)
        spin_box.setSingleStep(self._step)  # type: ignore
        spin_box.setMaximum(self._max_value)  # type: ignore
        return spin_box

class ConfigComboBox(ConfigBasedWidget):
    def __init__(
        self,
        config_field: ImmutableField[str],
        parent: Optional[QWidget] = None,
        allowed_values: List[Any] = [],
    ) -> None:
        super().__init__(config_field, parent)
        self._allowed_values = allowed_values
        self._combo_box = self._init_combo_box()
        self.widget: Final[QComboBox] = self._combo_box
        self.reset()

    def _init_combo_box(self) -> QComboBox:
        combo_box = QComboBox()
        combo_box.setObjectName(self.config_field.name)
        return combo_box

    def reset(self):
        self._combo_box.clear()
        self._combo_box.addItems(self._allowed_values)
        self.set(self.config_field.read())

    def read(self):
        return self._combo_box.currentText()

    def set(self, value):
        return self._combo_box.setCurrentText(value)


class ConfigFormLayout(QFormLayout):
    """Dialog zone consisting of spin boxes."""

    def __init__(self, elements: List[Union[ConfigBasedWidget, str]]) -> None:
        super().__init__()
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
        self.addRow(element.config_field.name, element.widget)

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addRow(QSplitter(Qt.Horizontal))
        self.addRow(label)

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for element in self._widgets:
            element.reset()

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for element in self._widgets:
            element.save()


class ConfigFormWidget(QWidget):
    def __init__(self, elements: List[Union[ConfigBasedWidget, str]]) -> None:
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
