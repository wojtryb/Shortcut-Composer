# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, Generic, TypeVar
from PyQt5.QtGui import QColor
from api_krita import Krita
from config_system import Field, FieldGroup
from config_system.field_base_impl import DualField, FieldWithEditableDefault
from data_components import Tag, PieDeadzoneStrategy
from core_components import Controller
from .group_manager_impl import dispatch_group_manager

T = TypeVar("T")
U = TypeVar("U")


class PieConfig(FieldGroup, Generic[T]):
    """
    FieldGroup representing config of PieMenu.

    Most of PieMenu components can read and modify this object to
    personalize it and remember its state between sessions.

    It contains conveniance methods that affect multiple fields at once.
    """

    def __init__(
        self,
        name: str,
        values: Tag | list[T],
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
        self._controller = controller
        self._manager = dispatch_group_manager(controller)

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

        tag_mode = isinstance(values, Tag)
        self.TAG_MODE = self._create_editable_dual_field(
            field_name="Tag mode",
            default=tag_mode)
        """If true, the pie operates on groups, not individual values."""

        tag_name = values.tag_name if isinstance(values, Tag) else ""
        self.TAG_NAME = self._create_editable_dual_field(
            field_name="Tag",
            default=tag_name)
        """Name of selected group if in group mode."""

        self.LAST_TAG_SELECTED = self.field(
            name="Last tag selected",
            default="---Select tag---")
        """Last selected value group remembered between sessions"""

        default_values = [] if isinstance(values, Tag) else values
        self.ORDER = self._create_editable_dual_field(
            field_name="Values",
            default=default_values,
            parser_type=controller.TYPE)
        """
        Selected values in specific order.

        - In group mode, specifies the order of the values.
        - In manual mode, specifies both the values and their order.
        """

    @property
    def allow_value_edit(self) -> bool:
        """Return whether user can add and remove items from the pie."""
        return not self.TAG_MODE.read()

    def values(self) -> list[T]:
        """Return all presets based on mode and stored order."""
        if not self.TAG_MODE.read():
            return self.ORDER.read()

        return self._manager.get_values(self.TAG_NAME.read())

    def set_values(self, values: list[T]) -> None:
        """When in tag mode, remember the tag order. Then write normally."""
        if self.TAG_MODE.read():
            group = "ShortcutComposer: Tag order"
            field = Field(
                group, self.TAG_NAME.read(), [], self._controller.TYPE)
            field.write(values)

        self.ORDER.write(values)

    def refresh_order(self) -> None:
        """Refresh the values in case the active document changed."""
        self.TAG_MODE.field.refresh()
        self.TAG_NAME.field.refresh()
        self.ORDER.write(self.values())

    def set_current_as_default(self) -> None:
        """Set current pie values as a new default list of values."""
        self.TAG_MODE.default = self.TAG_MODE.read()
        self.TAG_NAME.default = self.TAG_NAME.read()
        self.ORDER.default = self.ORDER.read()

    def reset_the_default(self) -> None:
        """Set empty pie as a new default list of values."""
        self.TAG_MODE.default = False
        self.TAG_NAME.default = ""
        self.ORDER.default = []

    def reset_to_default(self) -> None:
        """Replace current list of values in pie with the default list."""
        self.TAG_MODE.reset_default()
        self.TAG_NAME.reset_default()
        self.ORDER.reset_default()
        self.refresh_order()

    def is_order_default(self) -> bool:
        """Return whether order is the same as default one."""
        return (
            self.TAG_MODE.read() == self.TAG_MODE.default
            and self.TAG_NAME.read() == self.TAG_NAME.default
            and self.ORDER.read() == self.ORDER.default)

    def register_to_order_related(self, callback: Callable[[], None]) -> None:
        """Register callback to all fields related to value order."""
        self.TAG_MODE.register_callback(callback)
        self.TAG_NAME.register_callback(callback)
        self.ORDER.register_callback(callback)

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
