from typing import Dict, Union
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
)

from ..config import Config
from ..krita_setting import write_setting


class Forms(QFormLayout):

    def __init__(self):
        super().__init__()
        self.forms: Dict[Config, Union[QSpinBox, QDoubleSpinBox]] = {}

        def add_row(config: Config, is_int: bool):
            form = self._create_form(config, is_int)
            self.addRow(config.value, form)

        add_row(Config.SHORT_VS_LONG_PRESS_TIME, is_int=False)
        add_row(Config.SLIDER_SENSITIVITY_SCALE, is_int=False)
        add_row(Config.SLIDER_DEADZONE, is_int=True)
        add_row(Config.FPS_LIMIT, is_int=True)
        add_row(Config.PIE_GLOBAL_SCALE, is_int=False)
        add_row(Config.PIE_ICON_GLOBAL_SCALE, is_int=False)
        add_row(Config.PIE_DEADZONE_GLOBAL_SCALE, is_int=False)

    def refresh(self):
        for config, form in self.forms.items():
            form.setValue(float(config.get()))  # type: ignore

    def apply(self):
        for form in self.forms.values():
            write_setting(
                name=form.objectName(),
                value=form.value()
            )

    def _create_form(self, config: Config, is_int: bool):
        form = QSpinBox() if is_int else QDoubleSpinBox()
        form.setObjectName(config.value)
        form.setMinimum(0)
        form.setSingleStep(1 if is_int else 0.1)  # type: ignore

        self.forms[config] = form
        return form
