# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Generic, TypeVar

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

    @property
    def deadzone_radius(self) -> int:
        return round(self.DEADZONE_SCALE.read() * 100)

    @property
    def widget_radius(self) -> int:
        return round(self.deadzone_radius + self.INNER_ZONE_SCALE.read() * 75)
