# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import Enum

from core_components import Controller
from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from templates.pie_menu_utils import PieSettings
from ..pie_style_holder import PieStyleHolder
from ..pie_label import PieLabel
from shortcut_composer.composer_utils.label.complex_widgets import ScrollArea


class EnumPieSettings(PieSettings):
    """
    Pie setting window for pie values being enums.

    Consists of two tabs:
    - usual form with field values to set
    - scrollable area with all available enum values to drag into pie
    """

    def __init__(
        self,
        controller: Controller[Enum],
        config: NonPresetPieConfig,
        style_holder: PieStyleHolder,
        *args, **kwargs
    ) -> None:
        super().__init__(config, style_holder)

        names = controller.TYPE._member_names_
        values = [controller.TYPE[name] for name in names]
        labels = [PieLabel.from_value(value, controller) for value in values]
        labels = [label for label in labels if label is not None]

        self._action_values = ScrollArea[PieLabel](
            self._style_holder.unscaled_label_style, 3)
        self._action_values.replace_handled_labels(labels)
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie non draggable and disabled."""
        self._action_values.mark_used_values(self._config.values())
