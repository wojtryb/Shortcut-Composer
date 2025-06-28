# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from ..pie_label import PieLabel
from ..pie_value_manager import PieValueManager
from ..pie_config import PieConfig
from composer_utils import GroupOrderHolder


class EnumPieValueManager(PieValueManager):
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._group_order_holder = GroupOrderHolder(controller.TYPE)
        self._enum_type = self._controller.TYPE

    def fetch_groups(self) -> list[str]:
        return list(self._enum_type._groups_.keys())

    def labels_from_values(
        self,
        values: list[EnumGroup]
    ) -> list[PieLabel[EnumGroup]]:
        """Create labels from list of preset names."""
        labels = [PieLabel.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]

    def labels_from_group(
        self,
        group: str,
        sort: bool = True
    ) -> list[PieLabel]:
        return self.labels_from_values(self._get_values(group, sort))

    def labels_from_config(self, config: PieConfig) -> list[PieLabel]:
        if not config.TAG_MODE.read():
            values = config.ORDER.read()
        else:
            values = self._get_values(config.TAG_NAME.read())
        return self.labels_from_values(values)

    def _get_values(
        self,
        group: str,
        sort: bool = True
    ) -> list[EnumGroup]:
        if group == "All":
            return list(self._enum_type._member_map_.values())
        elif group not in self._enum_type._groups_:
            return []

        from_krita = self._enum_type._groups_[group]
        if not sort:
            return from_krita
        from_config = self._group_order_holder.get_order(group)

        known_order = [v for v in from_config if v in from_krita]
        missing = [v for v in from_krita if v not in from_config]

        return known_order + missing
