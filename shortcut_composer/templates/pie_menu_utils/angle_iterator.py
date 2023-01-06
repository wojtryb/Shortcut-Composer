import math

from PyQt5.QtCore import QPoint


class AngleIterator:
    def __init__(self, center_distance: int, radius: int, amount: int) -> None:
        self._center_distance = center_distance
        self._radius = radius
        self._amount = amount

    def __iter__(self):
        for angle in range(0, 360, round(360/self._amount)):
            yield angle, self._center_from_angle(angle)

    def _center_from_angle(self, angle: int) -> QPoint:
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._center_distance + self._radius*math.sin(rad_angle)),
            round(self._center_distance - self._radius*math.cos(rad_angle)),
        )
