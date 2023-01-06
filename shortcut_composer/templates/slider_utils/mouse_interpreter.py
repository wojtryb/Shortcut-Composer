from dataclasses import dataclass


@dataclass
class MouseInterpreter:

    min: float
    max: float
    mouse_origin: float
    start_value: float
    sensitivity: float

    def mouse_to_value(self, mouse: int) -> float:
        value = self.start_value + self._delta(mouse)
        self._recalibrate(value)
        return self._clip(value)

    def _recalibrate(self, value) -> None:
        delta = (self.min - value)*self.sensitivity
        if delta > 0:
            self.mouse_origin -= delta

        delta = (self.max - value)*self.sensitivity
        if delta < 0:
            self.mouse_origin -= delta

    def _delta(self, mouse: int) -> float:
        return (mouse - self.mouse_origin)/self.sensitivity

    def _clip(self, value) -> float:
        return min(
            max(self.min, value),
            self.max
        )
