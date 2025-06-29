# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar
from PyQt5.QtGui import QColor
from api_krita import Krita
from core_components import Controller
from config_system import FieldGroup
from config_system.field_base_impl import DualField, FieldWithEditableDefault
from data_components import Group, PieDeadzoneStrategy

T = TypeVar("T")
U = TypeVar("U")


class PieConfig(FieldGroup, Generic[T]):
    """
    FieldGroup representing config of PieMenu.

    Most of PieMenu components can read and modify this object to
    personalize it and remember its state between sessions.
    """

    def __init__(
        self,
        name: str,
        values: list[T] | Group,
        controller: Controller,
        pie_radius_scale: float,
        icon_radius_scale: float,
        save_local: bool,
        background_color: QColor | None,
        active_color: QColor | None,
        pie_opacity: int,
        deadzone_strategy: PieDeadzoneStrategy,
        max_lines_amount: int,
        max_signs_amount: int,
        abbreviate_with_dot: bool,
    ) -> None:
        super().__init__(name)

        self.PIE_RADIUS_SCALE = self.field(
            name="Pie scale",
            default=pie_radius_scale)
        """Local scale of the pie applied on top of global one."""
        self.ICON_RADIUS_SCALE = self.field(
            name="Icon scale",
            default=icon_radius_scale)
        """Local scale of the labels applied on top of global one."""

        self.SAVE_LOCAL = self.field(
            name="Save local",
            default=save_local)
        """If true, the values are stored in .kra instead of .kritarc."""
        self.DEADZONE_STRATEGY = self.field(
            name="deadzone",
            default=deadzone_strategy)
        """Specifies what to do, when pie is closed with mouse on deadzone."""

        # override the krita theme if at least one color is given.
        override_krita_theme = bool(active_color or background_color)
        if background_color is None:
            background_color = Krita.get_main_color_from_theme()
        if active_color is None:
            active_color = Krita.get_active_color_from_theme()

        self.OVERRIDE_DEFAULT_THEME = self.field(
            name="Override default theme",
            default=override_krita_theme)
        """If true, given colors are used instead of those from krita theme."""
        self.BACKGROUND_COLOR = self.field(
            name="Background color",
            default=background_color)
        """Color of pie background if theme is overridden."""
        self.ACTIVE_COLOR = self.field(
            name="Active color",
            default=active_color)
        """Color of active label if theme is overridden."""
        self.PIE_OPACITY = self.field(
            name="Pie opacity",
            default=pie_opacity)
        """Opacity of the pie background."""
        self.MAX_LINES_AMOUNT = self.field(
            name="Max lines amount",
            default=max_lines_amount)
        """Limit of lines of text inside labels."""
        self.MAX_SIGNS_AMOUNT = self.field(
            name="Max letters amount",
            default=max_signs_amount)
        """Limit of signs in the longest line of text inside labels."""
        self.ABBREVIATE_WITH_DOT = self.field(
            name="Abbreviate with dot",
            default=abbreviate_with_dot)
        """Sign used to show that text was trimmed."""

        group_mode = isinstance(values, Group)
        self.GROUP_MODE = self._create_editable_dual_field(
            field_name="Tag mode",  # Backwards compatibility
            default=group_mode)
        """If true, the pie operates on groups, not individual values."""

        group_name = values.group_name if isinstance(values, Group) else ""
        self.GROUP_NAME = self._create_editable_dual_field(
            field_name="Tag",
            default=group_name)
        """Name of selected group if in group mode."""

        self.LAST_GROUP_SELECTED = self.field(
            name="Last tag selected",
            default="---Select group---")
        """Last selected value group remembered between sessions."""
        self.LAST_VALUE_SELECTED = self.field(
            name="Last value selected",
            default=controller.DEFAULT_VALUE)
        """Last selected value remembered between sessions."""
        # TODO: if Field could exist without default, but with only
        # parser, controller here would not be needed.
        # Field should default to None, this class should get only TYPE

        default_values = [] if isinstance(values, Group) else values
        self.ORDER = self._create_editable_dual_field(
            field_name="Values",
            default=default_values,
            parser_type=controller.TYPE)
        """
        Selected values in specific order.

        - In group mode, specifies the order of the values.
        - In manual mode, specifies both the values and their order.
        """

    def _create_editable_dual_field(
        self,
        field_name: str,
        default: U,
        parser_type: type | None = None
    ) -> FieldWithEditableDefault[U, DualField[U]]:
        """Return field which can switch save location and default value."""
        return FieldWithEditableDefault(
            DualField(self, self.SAVE_LOCAL, field_name, default, parser_type),
            self.field(f"{field_name} default", default, parser_type))
