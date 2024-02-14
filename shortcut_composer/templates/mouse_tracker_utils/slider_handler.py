# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, Iterable, Generic, TypeVar

from api_krita import Krita
from api_krita.pyqt import Timer
from composer_utils import Config
from data_components import Slider, Range
from .new_types import MouseInput, Interpreted
from .mouse_interpreter import MouseInterpreter
from .slider_values import (
    RangeSliderValues,
    ListSliderValues,
    SliderValues,
)

T = TypeVar("T")
MouseGetter = Callable[[], MouseInput]


class SliderHandler(Generic[T]):
    """
    When started, tracks the mouse, interprets it and sets corresponding value.

    Arguments:
    - `slider`        -- configuration dataclass created by the user.
    - `is_horizontal` -- specifies which axis to track.

    On initialization, values to cycle stored in `slider` are wrapped in
    proper `SliderValues` which provides values compatible with the
    controller.

    The handler is running between `start()` and `stop()` calls.

    Right after start, the handler waits for the mouse to move past the
    deadzone, which allows to prevent unwanted changes.

    After the deadzone is reached, the value interpreter is created
    using the current mouse position.

    Main handler loop starts:
    - the mouse offset is being interpreted
    - interpreted values allow to fetch controller compatible values
      from the `SliderValues`
    - `SliderValues` values are being set using the controller.

    Calling stop cancels the process at any step, including deadzone
    phase in which case main loop will never be started.
    """

    def __init__(self, slider: Slider[T], is_horizontal: bool) -> None:
        """Store the slider configuration, create value adapter."""
        self._slider = slider
        self._to_cycle = self._create_slider_values(slider)
        self._is_horizontal = is_horizontal

        sleep_time = Config.get_sleep_time()
        self._deadzone_timer = Timer(
            target=self._start_after_deadzone,
            interval_ms=sleep_time)
        self._main_timer = Timer(
            target=self._value_setting_loop,
            interval_ms=sleep_time)

        self._mouse_getter: MouseGetter
        self._start_point: MouseInput
        self._interpreter: MouseInterpreter

    def start(self) -> None:
        """Start a deadzone phase in a timer."""
        self._working = True
        self._slider.controller.refresh()
        self._mouse_getter = self._pick_mouse_getter()
        self._start_point = self.read_mouse()
        self._deadzone_timer.start()

    def stop(self) -> None:
        """Stop a process by stopping any timers."""
        self._deadzone_timer.stop()
        self._main_timer.stop()

    def read_mouse(self) -> MouseInput:
        """Fetch current mouse position."""
        return self._mouse_getter()

    def _start_after_deadzone(self) -> None:
        """Block a thread until mouse reaches deadzone. Then start a loop."""
        current = self.read_mouse()
        if abs(self._start_point - current) <= self._slider.deadzone:
            return
        self._deadzone_timer.stop()
        self._update_interpreter()
        self._main_timer.start()

    def _value_setting_loop(self) -> None:
        """Set current value from `SliderValues`."""
        clipped_value = self._interpreter.interpret(self.read_mouse())
        to_set = self._to_cycle.at(clipped_value)
        self._slider.controller.set_value(to_set)

    def _update_interpreter(self) -> None:
        """Store a new interpreter with current mouse and current value."""
        self._interpreter = MouseInterpreter(
            min=self._to_cycle.min,
            max=self._to_cycle.max,
            mouse_origin=self.read_mouse(),
            start_value=self._get_current_interpreted_value(),
            pixels_in_unit=self._slider.pixels_in_unit,
        )

    def _get_current_interpreted_value(self) -> Interpreted:
        """Read interpreted value corresponding to currently set value."""
        controller_value = self._slider.controller.get_value()
        return self._to_cycle.index(controller_value)

    def _pick_mouse_getter(self) -> MouseGetter:
        """
        Refresh a mouse fetching method.

        This can't be done in plugin initialization phase, as the
        qwindow is not created at that point.

        Doing it once on every process start guarantees correct work
        even when the cursor object gets deleted by C++.
        """
        cursor = Krita.get_cursor()
        if self._is_horizontal:
            return lambda: MouseInput(cursor.x())
        return lambda: MouseInput(-cursor.y())

    @staticmethod
    def _create_slider_values(slider: Slider[T]) -> SliderValues[T]:
        """Return the right values adapter based on passed data type."""
        if isinstance(slider.values, Iterable):
            return ListSliderValues(slider.values)
        elif isinstance(slider.values, Range):
            return RangeSliderValues(slider.values)

        raise RuntimeError(f"Wrong type: {slider.values}")
