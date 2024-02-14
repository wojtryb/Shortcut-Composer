# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Generic, TypeVar, Optional

from PyQt5.QtGui import QColor

from api_krita import Krita
from config_system import FieldGroup

T = TypeVar("T")


class RotationConfig(FieldGroup, Generic[T]):

    def __init__(
        self,
        name: str,
        deadzone_scale: float,
        inner_zone_scale: float,
        divisions: int,
        inverse_zones: bool,
        active_color: Optional[QColor],
        is_counterclockwise: bool,
        offset: int,
    ) -> None:
        super().__init__(name)

        self.DEADZONE_SCALE = self.field(
            name="Deadzone scale",
            default=deadzone_scale)

        self.INNER_ZONE_SCALE = self.field(
            name="Inner zone scale",
            default=inner_zone_scale)

        self.DIVISIONS = self.field(
            name="Divisions",
            default=divisions)

        self.INVERSE_ZONES = self.field(
            name="Inverse zones",
            default=inverse_zones)

        if active_color is None:
            active_color = Krita.get_active_color_from_theme()
        self.ACTIVE_COLOR = self.field(
            name="Active color",
            default=active_color)

        self.IS_COUNTERCLOCKWISE = self.field(
            name="Is counterclockwise",
            default=is_counterclockwise)

        self.OFFSET = self.field(
            name="Offset",
            default=offset)
