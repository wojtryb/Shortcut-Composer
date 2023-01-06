from dataclasses import dataclass

from .new_types import MouseInput, Interpreted


@dataclass
class MouseInterpreter:

    min: Interpreted
    max: Interpreted
    mouse_origin: MouseInput
    start_value: Interpreted
    min: Interpreted
    max: Interpreted
    pixels_in_unit: float

    def interpret(self, mouse: MouseInput) -> Interpreted:
        mouse_delta = MouseInput(mouse - self.mouse_origin)
        value_delta = self.mouse_to_value(mouse_delta)
        raw_value = Interpreted(self.start_value + value_delta)
        self._recalibrate_if_needed(raw_value)
        return self._clip(raw_value)

    def _recalibrate_if_needed(self, value: Interpreted) -> None:
        if (middle := self._clip(value)) == value:
            return
        value_delta = Interpreted(middle - value)
        mouse_delta = self.value_to_mouse(value_delta)
        self.mouse_origin = MouseInput(self.mouse_origin - mouse_delta)

    def mouse_to_value(self, mouse: MouseInput) -> Interpreted:
        return Interpreted(mouse/self.pixels_in_unit)

    def value_to_mouse(self, value: Interpreted) -> MouseInput:
        return MouseInput(round(value*self.pixels_in_unit))

    def _clip(self, value: Interpreted) -> Interpreted:
        return sorted((self.min, value, self.max))[1]
