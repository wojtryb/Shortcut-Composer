from typing import Dict
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QSpinBox,
    QLabel,
)
from PyQt5.QtCore import Qt
from dataclasses import dataclass
from typing import Dict, Union
from PyQt5.QtWidgets import QWidget

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

from .pie_config import PieConfig
from composer_utils import ConfigBase

SpinBox = Union[QSpinBox, QDoubleSpinBox]


class LocalPieSettings(QWidget):
    """Dialog which allows to change global settings of the plugin."""

    def __init__(self, pie_config: PieConfig) -> None:
        super().__init__()
        self._pie_config = pie_config

        self._layouts_dict = {
            "SpinBoxes": SpinBoxesLayout(pie_config),
        }
        layout = QVBoxLayout()
        for layout_part in self._layouts_dict.values():
            layout.addLayout(layout_part)

        stretched = QHBoxLayout()
        stretched.addStretch()
        stretched.addLayout(layout)
        stretched.addStretch()
        self.setLayout(stretched)

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        for layout in self._layouts_dict.values():
            layout.apply()

    def refresh(self) -> None:
        """Ask all dialog zones to refresh themselves. """
        for layout in self._layouts_dict.values():
            layout.refresh()


class SpinBoxesLayout(QFormLayout):
    """Dialog zone consisting of spin boxes."""

    @dataclass
    class ConfigParams:
        """Adds spinbox parametrization to the config field."""
        config: ConfigBase
        step: float
        max_value: float
        is_int: bool

    def __init__(self, pie_config: PieConfig) -> None:
        super().__init__()
        self._forms: Dict[ConfigBase, SpinBox] = {}
        
        self._add_label("Bla")

        self._add_row(self.ConfigParams(
            pie_config.pie_radius_scale,
            step=0.05,
            max_value=4,
            is_int=False))
        self._add_row(self.ConfigParams(
            pie_config.icon_radius_scale,
            step=0.05,
            max_value=4,
            is_int=False))

        self._add_label("Ble")

    def _add_row(self, config_params: ConfigParams) -> None:
        """Add a spin box to the layout along with its description."""
        self.addRow(
            config_params.config.name,
            self._create_form(config_params))

    def _add_label(self, text: str):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        self.addRow(QSplitter(Qt.Horizontal))
        self.addRow(label)

    def _create_form(self, config_params: ConfigParams) -> SpinBox:
        """Store and return new spin box for required type (int or float)."""
        form = QSpinBox() if config_params.is_int else QDoubleSpinBox()
        form.setObjectName(config_params.config.name)
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
