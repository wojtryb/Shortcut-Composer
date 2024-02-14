# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import math
from typing import Iterable, Tuple

from PyQt5.QtCore import QPoint


class CirclePoints:
    """
    Operates on points located on a provided circle.

    Initialized with values describing a circle:
    - center -- point being the circle center
    - radius -- radius of a circle

    Allows to:
    - calculate distance from the circle center
    - transform between angle and related point on the circle
    - iterate over points, when the circle is divided into even parts
    """

    def __init__(self, center: QPoint, radius: int) -> None:
        self._center = center
        self._radius = radius

    def distance(self, point: QPoint) -> float:
        """Count distance between pie center and cursor position."""
        distance = (self._center.x() - point.x()) ** 2
        distance += (self._center.y() - point.y()) ** 2
        return distance ** 0.5

    def point_from_angle(self, angle: float) -> QPoint:
        """Return a point located at given angle."""
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._center.x() + self._radius*math.sin(rad_angle)),
            round(self._center.y() - self._radius*math.cos(rad_angle)))

    def angle_from_point(self, point: QPoint) -> float:
        """Count clockwise angle of cursor in relation to pie center."""
        return math.degrees(math.atan2(
            -self._center.x() + point.x(),
            self._center.y() - point.y()
        )) % 360

    def iterate_over_circle(self, amount: int) -> Iterable[Tuple[int, QPoint]]:
        """Iterate over points, when the circle is divided into even parts."""
        for angle in self._float_range(0, 360, 360/amount):
            yield round(angle), self.point_from_angle(angle)

    @staticmethod
    def _float_range(start: float, end: float, step: float) -> Iterable[float]:
        """Implementation of range() which supports `step` being float."""
        while start < end:
            yield start
            start += step
