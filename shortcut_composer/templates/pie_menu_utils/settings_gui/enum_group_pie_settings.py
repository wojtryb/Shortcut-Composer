# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from config_system import Field
from ..label import Label
from ..pie_style import PieStyle
from ..pie_config import NonPresetPieConfig
from .pie_settings import PieSettings
from .scroll_area import ScrollArea
from .components import GroupComboBox, EnumGroupFetcher, GroupFetcher


class GroupScrollArea(ScrollArea):
    def __init__(
        self,
        controller: Controller[EnumGroup],
        fetcher: GroupFetcher,
        style: PieStyle,
        columns: int,
        field: Field,
        parent=None
    ) -> None:
        super().__init__(style, columns, parent)
        self._controller = controller
        self._field = field
        self._fetcher = fetcher
        self.group_chooser = GroupComboBox(
            config_field=self._field,
            group_fetcher=self._fetcher,
            additional_fields=["All"])
        self.group_chooser.widget.currentTextChanged.connect(
            self._display_group)
        self._layout.insertWidget(0, self.group_chooser.widget)
        self._display_group()

    def _display_group(self) -> None:
        """Update preset widgets according to tag selected in combobox."""
        picked_group = self.group_chooser.widget.currentText()
        values = self._fetcher.get_values(picked_group)
        self.replace_handled_labels(self._fetcher.create_labels(values))
        self._apply_search_bar_filter()
        self.group_chooser.save()


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
            field=self._config.field("Last tag selected", "All"))
        self._action_values.replace_handled_labels(labels)
        self._tab_holder.insertTab(1, self._action_values, "Values")
        self._tab_holder.setCurrentIndex(1)

        self._config.ORDER.register_callback(self._refresh_draggable)
        self._refresh_draggable()

    def _refresh_draggable(self) -> None:
        """Make all values currently used in pie undraggable and disabled."""
        self._action_values.mark_used_values(self._config.values())

    # def create_labels(self, values: List[Enum]) -> List[Label[Enum]]:
    #     """Create labels from list of preset names."""
    #     labels = [Label.from_value(v, self._controller) for v in values]
    #     return [label for label in labels if label is not None]
