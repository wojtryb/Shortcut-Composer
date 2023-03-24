# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List, Union, Final, Optional
from PyQt5.QtWidgets import QDoubleSpinBox, QComboBox, QSpinBox, QWidget

from ..field import Field
from .config_based_widget import ConfigBasedWidget


class ConfigSpinBox(ConfigBasedWidget):
    def __init__(
        self,
        config_field: Union[Field[int], Field[float]],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        step: float = 1,
        max_value: float = 100,
    ) -> None:
        super().__init__(config_field, parent, pretty_name)
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
        spin_box = (QSpinBox() if type(self.config_field.default) is int
                    else QDoubleSpinBox())
        spin_box.setMinimumWidth(90)
        spin_box.setObjectName(self.config_field.name)
        spin_box.setMinimum(0)
        spin_box.setSingleStep(self._step)  # type: ignore
        spin_box.setMaximum(self._max_value)  # type: ignore
        return spin_box


class ConfigComboBox(ConfigBasedWidget):
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
