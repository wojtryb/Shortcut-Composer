# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QSplitter,
    QSpinBox,
    QLabel,
)

from ..config import Config

SpinBox = Union[QSpinBox, QDoubleSpinBox]


class SpinBoxesLayout(QFormLayout):
    """Dialog zone consisting of spin boxes."""

    def __init__(self) -> None:
        super().__init__()
        self._forms: Dict[Config, SpinBox] = {}

        self._add_label("Common settings")
        self._add_row(Config.SHORT_VS_LONG_PRESS_TIME, step=0.05, max_value=5, is_int=False)
        self._add_row(Config.FPS_LIMIT, step=10, max_value=300, is_int=True)

        self._add_label("Cursor trackers")
        self._add_row(Config.TRACKER_SENSITIVITY_SCALE, step=0.05, max_value=10, is_int=False)
        self._add_row(Config.TRACKER_DEADZONE, step=1, max_value=99, is_int=True)

        self._add_label("Pie menus display")
        self._add_row(Config.PIE_GLOBAL_SCALE, step=0.05, max_value=10, is_int=False)
        self._add_row(Config.PIE_ICON_GLOBAL_SCALE, step=0.05, max_value=10, is_int=False)
        self._add_row(Config.PIE_DEADZONE_GLOBAL_SCALE, step=0.05, max_value=10, is_int=False)
        self._add_row(Config.PIE_ANIMATION_TIME, step=0.05, max_value=10, is_int=False)

    def _add_row(self, config: Config, step: float, max_value: float, is_int: bool) -> None:
        """Add a spin box to the layout along with its description."""
        self.addRow(config.value, self._create_form(config, step, max_value, is_int))

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addRow(QSplitter(Qt.Horizontal))
        self.addRow(label)

    def _create_form(self, config: Config, step: float, max_value: float, is_int: bool) -> SpinBox:
        """Store and return new spin box for required type (int or float)."""
        form = QSpinBox() if is_int else QDoubleSpinBox()
        form.setObjectName(config.value)
        form.setMinimum(0)
        form.setSingleStep(step)  # type: ignore
        form.setMaximum(max_value)

        self._forms[config] = form
        return form

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for config, form in self._forms.items():
            form.setValue(config.read())  # type: ignore

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for config, form in self._forms.items():
            config.write(form.value())
