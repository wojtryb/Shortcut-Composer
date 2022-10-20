from dataclasses import dataclass

from .slider_values import SliderValues


@dataclass
class MouseInterpreter:

    to_cycle: SliderValues
    sensitivity: float

    def __post_init__(self):
        self.origin: float
        self.start_value: float

    def mouse_to_value(self, mouse: int) -> float:
        value = self.start_value + self._delta(mouse)
        self._recalibrate(value)
        return self._clip(value)

    def calibrate(self, mouse: int, value: float):
        self.origin = mouse
        self.start_value = value

    def _recalibrate(self, value):
        delta = (self.to_cycle.min - value)*self.sensitivity
        if delta > 0:
            self.origin -= delta

        delta = (self.to_cycle.max - value)*self.sensitivity
        if delta < 0:
            self.origin -= delta

    def _delta(self, mouse: int):
        return (mouse - self.origin)/self.sensitivity

    def _clip(self, value):
        return min(
            max(self.to_cycle.min, value),
            self.to_cycle.max
        )
