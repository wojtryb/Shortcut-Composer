# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional, Type
from enum import Enum

from PyQt5.QtWidgets import QWidget

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from config_system import Field
from config_system.ui import ConfigComboBox
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import NonPresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea


class GroupComboBox(ConfigComboBox):
    def __init__(
        self,
        config_field: Field[str],
        enum_type: Type[EnumGroup],
        parent: Optional[QWidget] = None,
        pretty_name: Optional[str] = None,
        additional_fields: List[str] = [],
    ) -> None:
        self._additional_fields = additional_fields
        self._enum_type = enum_type
        super().__init__(config_field, parent, pretty_name)
        self.config_field.register_callback(
            lambda: self.set(self.config_field.read()))

    def reset(self) -> None:
        """Replace list of available tags with those red from database."""
        self._combo_box.clear()
        self._combo_box.addItems(self._additional_fields)
        self._combo_box.addItems(self._enum_type._groups_.keys())
        self.set(self.config_field.read())


class GroupScrollArea(ScrollArea):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        style: PieStyle,
        columns: int,
        field: Field,
        parent=None
    ) -> None:
        super().__init__(style, columns, parent)
        self._controller = controller
        self._field = field
        self.group_chooser = GroupComboBox(
            self._field,
            enum_type=self._controller.TYPE,
            additional_fields=["All"])
        self.group_chooser.widget.currentTextChanged.connect(
            self._display_group)
        self._layout.insertWidget(0, self.group_chooser.widget)
        self._display_group()

    def _display_group(self) -> None:
        """Update preset widgets according to tag selected in combobox."""
        picked_group = self.group_chooser.widget.currentText()
        if picked_group == "All":
            values = list(self._controller.TYPE._member_map_.values())
        else:
            values = self._controller.TYPE._groups_[picked_group]

        self.replace_handled_labels(self._create_labels(values))
        self._apply_search_bar_filter()
        self.group_chooser.save()

    def _create_labels(self, values: List[Enum]) -> List[Label[Enum]]:
        """Create labels from list of preset names."""
        labels = [Label.from_value(v, self._controller) for v in values]
        return [label for label in labels if label is not None]


class EnumGroupPieSettings(PieSettings):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        config: NonPresetPieConfig,
        style: PieStyle,
    ) -> None:
        super().__init__(config, style)

        names = controller.TYPE._member_names_
        values = [controller.TYPE[name] for name in names]
        labels = [Label.from_value(value, controller) for value in values]
        labels = [label for label in labels if label is not None]

        self._action_values = GroupScrollArea(
            controller=controller,
            style=self._style,
            columns=3,
            field=self._config.field("Last tag selected", "All"))
        self._action_values.replace_handled_labels(labels)
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_values(self._config.values())
