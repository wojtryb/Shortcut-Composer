# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Generic, TypeVar

from PyQt5.QtGui import QColor

from api_krita import Krita
from config_system import FieldGroup
from data_components import RotationDeadzoneStrategy

T = TypeVar("T")


class RotationConfig(FieldGroup, Generic[T]):
    """FieldGroup representing config of RotationSelector."""

    def __init__(
        self,
        name: str,
        is_widget_hidden: bool,
        deadzone_strategy: RotationDeadzoneStrategy,
        inverse_zones: bool,
        divisions: int,
        deadzone_scale: float,
        inner_zone_scale: float,
        active_color: QColor | None,
        outline_opacity: int,
        is_counterclockwise: bool,
        offset: int,
    ) -> None:
        super().__init__(name)

        self.IS_WIDGET_HIDDEN = self.field(
            name="Is widget hidden",
            default=is_widget_hidden)

        self.DEADZONE_STRATEGY = self.field(
            name="Deadzone strategy",
            default=deadzone_strategy)

        self.INVERSE_ZONES = self.field(
            name="Inverse zones",
            default=inverse_zones)

        self.DIVISIONS = self.field(
            name="Divisions",
            default=divisions)

        self.DEADZONE_SCALE = self.field(
            name="Deadzone scale",
            default=deadzone_scale)

        self.INNER_ZONE_SCALE = self.field(
            name="Inner zone scale",
            default=inner_zone_scale)

        if active_color is None:
            active_color = Krita.get_active_color_from_theme()
        self.ACTIVE_COLOR = self.field(
            name="Active color",
            default=active_color)

        self.OUTLINE_OPACITY = self.field(
            name="Outline opacity",
            default=outline_opacity)

        self.IS_COUNTERCLOCKWISE = self.field(
            name="Is counterclockwise",
            default=is_counterclockwise)

        self.OFFSET = self.field(
            name="Offset",
            default=offset)
