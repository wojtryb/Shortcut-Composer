# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import NonPresetPieConfig
from .pie_settings import PieSettings
from .components import EnumGroupFetcher, GroupScrollArea


class EnumGroupPieSettings(PieSettings):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        config: NonPresetPieConfig,
        style: PieStyle,
    ) -> None:
        super().__init__(config, style)

        self._controller = controller
        names = controller.TYPE._member_names_
        values = [controller.TYPE[name] for name in names]
        labels = [Label.from_value(value, controller) for value in values]
        labels = [label for label in labels if label is not None]

        self._action_values = GroupScrollArea(
            controller=controller,
            fetcher=EnumGroupFetcher(self._controller),
            style=self._style,
            columns=3,
            field=self._config.field("Last tag selected", "All"),
            additional_fields=["All"])
        self._action_values.replace_handled_labels(labels)
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_values(self._config.values())
