# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from core_components import NumericController
from composer_utils.label.complex_widgets import NumericValuePicker

from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from templates.pie_menu_utils import PieSettings
from ..pie_style_holder import PieStyleHolder
from ..pie_label import PieLabel


class NumericPieSettings(PieSettings):
    """Pie setting window for pie values being numeric (int)."""

    def __init__(
        self,
        controller: NumericController,
        config: NonPresetPieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        super().__init__(config, style_holder)

        def label_from_integer(value: int) -> PieLabel[int]:
            label = PieLabel.from_value(value, controller)
            if label is None:
                raise RuntimeError(f"Could not create label from {value}")
            return label

        self._numeric_picker = NumericValuePicker(
            create_label_from_integer=label_from_integer,
            unscaled_label_style=style_holder.unscaled_label_style,
            min_value=controller.MIN_VALUE,
            max_value=controller.MAX_VALUE,
            step=controller.STEP,
            wrapping=controller.WRAPPING,
            adaptive=controller.ADAPTIVE)

        self._tab_holder.insertTab(1, self._numeric_picker, "Values")
        self._tab_holder.setCurrentIndex(1)
