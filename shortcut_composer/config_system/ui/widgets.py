# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from typing import Any, List, Final, Optional, TypeVar, Generic, Protocol, Type
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QComboBox,
    QSpinBox,
    QWidget,
    QPushButton,
    QColorDialog)
from PyQt5.QtGui import QColor

from ..field import Field
from .config_based_widget import ConfigBasedWidget

F = TypeVar("F", bound=float)
E = TypeVar("E", bound=Enum)


class SpinBox(Protocol, Generic[F]):
    """Representation of both Qt spinboxes as one generic class."""

    def value(self) -> F: ...
    def setValue(self, val: F) -> None: ...


class ConfigSpinBox(ConfigBasedWidget[F]):
    """
    Wrapper of SpinBox linked to a configutation field.

    Based on QSpinBox or QDoubleSpinBox depending on the config type.
    Works only for fields of type: `int` or `float`.
    """

    def __init__(
        self,
        config_field: Field[F],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        step: F = 1,
        max_value: F = 100,
    ) -> None:
        super().__init__(config_field, parent, pretty_name)
        self._step = step
        self._max_value = max_value
        self._spin_box = self._init_spin_box()
        self.widget: Final[SpinBox[F]] = self._spin_box
        self.reset()

    def read(self) -> F:
        """Return the current value of the spinbox widget."""
        return self._spin_box.value()

    def set(self, value: F) -> None:
        """Replace the value of the spinbox widget with passed one."""
        self._spin_box.setValue(value)

    def _init_spin_box(self) -> SpinBox:
        """Return the spinbox widget of type based on config field type."""
        spin_box: QDoubleSpinBox = {int: QSpinBox, float: QDoubleSpinBox}[
            type(self.config_field.default)]()

        spin_box.setMinimumWidth(90)
        spin_box.setObjectName(self.config_field.name)
        spin_box.setMinimum(0)
        spin_box.setSingleStep(self._step)
        spin_box.setMaximum(self._max_value)
        return spin_box


class ConfigComboBox(ConfigBasedWidget[str]):
    """
    Wrapper of Combobox linked to a configutation field.

    Works only for fields of type: `str`.
    """

    def __init__(
        self,
        config_field: Field[str],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        allowed_values: List[Any] = [],
    ) -> None:
        super().__init__(config_field, parent, pretty_name)
        self._allowed_values = allowed_values
        self._combo_box = self._init_combo_box()
        self.widget: Final[QComboBox] = self._combo_box
        self.reset()

    def reset(self) -> None:
        """Update allowed values of the combobox and pick a default one."""
        self._combo_box.clear()
        self._combo_box.addItems(self._allowed_values)
        self.set(self.config_field.read())

    def read(self) -> str:
        """Return the current value of the ComboBox."""
        return self._combo_box.currentText()

    def set(self, value: str) -> None:
        """Replace the value of the ComboBox with passed one."""
        self._combo_box.setCurrentText(value)

    def _init_combo_box(self) -> QComboBox:
        """Return the combobox widget."""
        combo_box = QComboBox()
        combo_box.setObjectName(self.config_field.name)
        return combo_box


class EnumComboBox(ConfigBasedWidget[E]):
    """
    Wrapper of Combobox linked to a Enum configutation field.

    Allows to pick one of enum members.
    """

    def __init__(
        self,
        config_field: Field[E],
        enum_type: Type[E],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
    ) -> None:
        super().__init__(config_field, parent, pretty_name)
        self._enum_type = enum_type
        self._combo_box = self._init_combo_box()
        self.widget: Final[QComboBox] = self._combo_box

        keys = list(self._enum_type._value2member_map_.keys())
        self._combo_box.addItems(keys)

        self.reset()

    def read(self) -> E:
        """Return Enum member selected with the combobox."""
        text = self._combo_box.currentText()
        return self._enum_type(text)

    def set(self, value: E) -> None:
        """Set the combobox to given Enum member."""
        self._combo_box.setCurrentText(value.value)

    def _init_combo_box(self) -> QComboBox:
        """Return the combobox widget."""
        combo_box = QComboBox()
        combo_box.setObjectName(self.config_field.name)
        return combo_box


class ColorButton(ConfigBasedWidget[QColor]):
    def __init__(
        self,
        config_field: Field[QColor],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
    ) -> None:
        super().__init__(config_field, parent, pretty_name)
        self._button = self._init_button()
        self._color = self.config_field.read()
        self.widget: Final[QPushButton] = self._button

        self.reset()

    def read(self) -> QColor:
        return self._color

    def set(self, value: QColor) -> None:
        self._color = value
        self._button.setStyleSheet(
            f"background-color: {self._color.name()}; border: none")

    def _init_button(self) -> QPushButton:
        def on_click():
            self.set(QColorDialog.getColor(self._color))

        button = QPushButton("")
        button.clicked.connect(on_click)
        return button
