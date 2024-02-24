# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum
from typing import Final, TypeVar, Generic, Protocol, Type

from PyQt5.QtWidgets import (
    QWidget,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QColorDialog,
    QDoubleSpinBox)
from PyQt5.QtGui import QColor

from ..field import Field
from .config_based_widget import ConfigBasedWidget

F = TypeVar("F", bound=float)
E = TypeVar("E", bound=Enum)


class SpinBoxInterface(Protocol, Generic[F]):
    """Representation of both Qt spin_boxes as one generic class."""

    def value(self) -> F: ...
    def setValue(self, val: F) -> None: ...
    def setEnabled(self, a0: bool) -> None: ...


class SpinBox(ConfigBasedWidget[F]):
    """
    Wrapper of SpinBox linked to a `float` configuration field.

    Based on QSpinBox or QDoubleSpinBox depending on the config type.
    Works only for fields of type: `int` or `float`.
    """

    def __init__(
        self,
        config_field: Field[F],
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        tooltip: str | None = None,
        step: F = 1,
        max_value: F = 100,
    ) -> None:
        super().__init__(config_field, parent, pretty_name, tooltip)
        self._step = step
        self._max_value = max_value
        self._spin_box = self._init_spin_box()
        self.widget: Final[SpinBoxInterface[F]] = self._spin_box
        self.reset()

    def read(self) -> F:
        """Return the current value of the spinbox widget."""
        return self._spin_box.value()

    def set(self, value: F) -> None:
        """Replace the value of the spinbox widget with passed one."""
        self._spin_box.setValue(value)

    def _init_spin_box(self) -> SpinBoxInterface:
        """Return the spinbox widget of type based on config field type."""
        spin_box: QDoubleSpinBox = {int: QSpinBox, float: QDoubleSpinBox}[
            type(self.config_field.default)]()

        spin_box.setMinimumWidth(90)
        spin_box.setObjectName(self.config_field.name)
        spin_box.setMinimum(0)
        spin_box.setSingleStep(self._step)
        spin_box.setMaximum(self._max_value)
        if self.tooltip is not None:
            spin_box.setToolTip(self.tooltip)
        return spin_box


class StringComboBox(ConfigBasedWidget[str]):
    """Wrapper of Combobox linked to a `str` configuration field."""

    def __init__(
        self,
        config_field: Field[str],
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        tooltip: str | None = None,
        allowed_values: list[str] = [],
    ) -> None:
        super().__init__(config_field, parent, pretty_name, tooltip)
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
        if self.tooltip is not None:
            combo_box.setToolTip(self.tooltip)
        return combo_box


class EnumComboBox(ConfigBasedWidget[E]):
    """
    Wrapper of Combobox linked to a `Enum` configuration field.

    Allows to pick one of enum members.
    """

    def __init__(
        self,
        config_field: Field[E],
        enum_type: Type[E],
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        tooltip: str | None = None,
    ) -> None:
        super().__init__(config_field, parent, pretty_name, tooltip)
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
        combo_box.setObjectName(self.config_field.name)
        if self.tooltip is not None:
            combo_box.setToolTip(self.tooltip)
        return combo_box


class ColorButton(ConfigBasedWidget[QColor]):
    """
    Wrapper of QPushButton linked to a `QColor` configuration field.

    Button displays currently selected color, and clicking activates a
    color picker for changing it.
    """

    def __init__(
        self,
        config_field: Field[QColor],
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        tooltip: str | None = None,
    ) -> None:
        super().__init__(config_field, parent, pretty_name, tooltip)
        self._button = self._init_button()
        self._color = self.config_field.read()
        self.widget: Final[QPushButton] = self._button

        self.reset()

    def read(self) -> QColor:
        """Return QColor displayed in the button."""
        return self._color

    def set(self, value: QColor) -> None:
        """Remember given color, and replace current button color with it."""
        self._color = value
        self._button.setStyleSheet(
            r"QToolTip {} "
            r"QPushButton {"
            f"    background-color: {self._color.name()}"
            r"}")

    def _init_button(self) -> QPushButton:
        """Return the QPushButton widget."""
        def on_click() -> None:
            """Set the selected color, if the dialog was not cancelled."""
            fetched_color = QColorDialog.getColor(self._color)
            if fetched_color.isValid():
                self.set(fetched_color)

        button = QPushButton("")
        policy = button.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        button.setSizePolicy(policy)
        button.clicked.connect(on_click)
        if self.tooltip is not None:
            button.setToolTip(self.tooltip)
        return button


class Checkbox(ConfigBasedWidget[bool]):
    """Wrapper of QCheckBox linked to a `bool` configuration field."""

    def __init__(
        self,
        config_field: Field[bool],
        parent: QWidget | None = None,
        pretty_name: str | None = None,
        tooltip: str | None = None,
    ) -> None:
        super().__init__(config_field, parent, pretty_name, tooltip)
        self._checkbox = QCheckBox()
        if self.tooltip is not None:
            self._checkbox.setToolTip(self.tooltip)
        self.widget: Final[QCheckBox] = self._checkbox
        self.reset()

    def read(self) -> bool:
        """Return checkbox state."""
        return self._checkbox.isChecked()

    def set(self, value: bool) -> None:
        """Set checkbox state."""
        self._checkbox.setChecked(value)
