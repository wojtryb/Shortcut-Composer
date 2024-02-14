# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .new_types import MouseInput, Interpreted


@dataclass
class MouseInterpreter:
    """
    Translates mouse input to float, based on offset from mouse origin.

    During the initialization, `mouse_origin` and `start_values` are
    stored. Then, each `interpret(mouse)` call interprets the passed
    mouse in relation to the initial values.

    Mouse the same as `mouse_origin` should return the `start_value`.
    Moving the mouse before and after the `mouse_origin` point would
    make the interpreted value smaller and greater respectively.

    Sensitivity is described with `pixels_in_unit` which tells how many
    pixels need to be moved from the `mouse_origin` to change the value
    by 1.0.

    Returned interpreted values need to be inside of range between `min`
    and `max`. When the limit is exceeded, the interpreter gets
    recalibrated. The `mouse_origin` is modified, so that the current
    value points to the range limit.
    """

    mouse_origin: MouseInput
    start_value: Interpreted
    min: Interpreted
    max: Interpreted
    pixels_in_unit: float

    def interpret(self, mouse: MouseInput) -> Interpreted:
        """Return value corresponding to the `mouse`."""
        mouse_delta = MouseInput(mouse - self.mouse_origin)
        value_delta = self.mouse_to_value(mouse_delta)
        raw_value = Interpreted(self.start_value + value_delta)
        self._recalibrate_if_needed(raw_value)
        return self._clip(raw_value)

    def _recalibrate_if_needed(self, value: Interpreted) -> None:
        """If interpreted value, exceeds the range limit, recalibrate."""
        if (middle := self._clip(value)) == value:
            return
        value_delta = Interpreted(middle - value)
        mouse_delta = self.value_to_mouse(value_delta)
        self.mouse_origin = MouseInput(self.mouse_origin - mouse_delta)

    def mouse_to_value(self, mouse: MouseInput) -> Interpreted:
        """Translate the mouse offset to value offset."""
        return Interpreted(mouse/self.pixels_in_unit)

    def value_to_mouse(self, value: Interpreted) -> MouseInput:
        """Translate the value offset to mouse offset."""
        return MouseInput(round(value*self.pixels_in_unit))

    def _clip(self, value: Interpreted) -> Interpreted:
        """Clip the value to limit range."""
        return sorted((self.min, value, self.max))[1]
