import math
from typing import Iterable, Tuple, Generator

from PyQt5.QtCore import QPoint


class AngleIterator:
    def __init__(self, center_distance: int, radius: int, amount: int):
        self._center_distance = center_distance
        self._radius = radius
        self._amount = amount

    def __iter__(self) -> Generator[Tuple[int, QPoint], None, None]:
        for angle in self._float_range(0, 360, 360/self._amount):
            yield round(angle), self.center_from_angle(angle)

    @staticmethod
    def _float_range(start: float, end: float, step: float) -> Iterable[float]:
        while start < end:
            yield start
            start += step

    def center_from_angle(self, angle: float) -> QPoint:
        rad_angle = math.radians(angle)
        return QPoint(
            round(self._center_distance + self._radius*math.sin(rad_angle)),
            round(self._center_distance - self._radius*math.cos(rad_angle)),
        )
