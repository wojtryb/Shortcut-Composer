# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List, Final, Optional, TypeVar, Generic, Protocol
from PyQt5.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QWidget

from ..field import Field
from .config_based_widget import ConfigBasedWidget

F = TypeVar("F", bound=float)


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

    def set(self, value: F):
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

    def set(self, value: str):
        """Replace the value of the ComboBox with passed one."""
        return self._combo_box.setCurrentText(value)

    def _init_combo_box(self) -> QComboBox:
        """Return the spinbox widget."""
        combo_box = QComboBox()
        combo_box.setObjectName(self.config_field.name)
        return combo_box
