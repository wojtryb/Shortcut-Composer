# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict, Union
from dataclasses import dataclass
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

    @dataclass
    class ConfigParams:
        """Adds spinbox parametrization to the config field."""
        config: Config
        step: float
        max_value: float
        is_int: bool

    def __init__(self) -> None:
        super().__init__()
        self._forms: Dict[Config, SpinBox] = {}

        self._add_label("Common settings")

        self._add_row(self.ConfigParams(
            Config.SHORT_VS_LONG_PRESS_TIME,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_row(self.ConfigParams(
            Config.FPS_LIMIT,
            step=5,
            max_value=300,
            is_int=True))

        self._add_label("Cursor trackers")

        self._add_row(self.ConfigParams(
            Config.TRACKER_SENSITIVITY_SCALE,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_row(self.ConfigParams(
            Config.TRACKER_DEADZONE,
            step=1,
            max_value=200,
            is_int=True))

        self._add_label("Pie menus display")

        self._add_row(self.ConfigParams(
            Config.PIE_GLOBAL_SCALE,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_row(self.ConfigParams(
            Config.PIE_ICON_GLOBAL_SCALE,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_row(self.ConfigParams(
            Config.PIE_DEADZONE_GLOBAL_SCALE,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_row(self.ConfigParams(
            Config.PIE_ANIMATION_TIME,
            step=0.01,
            max_value=1,
            is_int=False))

    def _add_row(self, config_params: ConfigParams) -> None:
        """Add a spin box to the layout along with its description."""
        self.addRow(
            config_params.config.value,
            self._create_form(config_params)
        )

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addRow(QSplitter(Qt.Horizontal))
        self.addRow(label)

    def _create_form(self, config_params: ConfigParams) -> SpinBox:
        """Store and return new spin box for required type (int or float)."""
        form = QSpinBox() if config_params.is_int else QDoubleSpinBox()
        form.setObjectName(config_params.config.value)
        form.setMinimum(0)
        form.setMaximum(config_params.max_value)  # type: ignore
        form.setSingleStep(config_params.step)  # type: ignore

        self._forms[config_params.config] = form
        return form

    def refresh(self) -> None:
        """Read values from krita config and apply them to stored boxes."""
        for config, form in self._forms.items():
            form.setValue(config.read())  # type: ignore

    def apply(self) -> None:
        """Write values from stored spin boxes to krita config file."""
        for config, form in self._forms.items():
            config.write(form.value())
