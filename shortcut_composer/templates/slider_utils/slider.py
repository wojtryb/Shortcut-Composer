from threading import Thread
from time import sleep
from typing import Any, Callable, List, Union

from components import Controller, InstructionHolder
from .mouse_interpreter import MouseInterpreter
from .slider_values import create_slider_values, Range


class Slider:
    """
    Part of MouseTracker specifying what to do on single axis movement.

    When the slider is started:
    - when controlled value belongs to `values_to_cycle`, it stays as is,
    - otherwise is set to `default_value`.

    While the slider is active the value is being changed relatively to
    the offset from the starting value.

    The `default_value` can be either:
    -  a discrete list of values
    -  a contiguous range defined using Range(start, stop)

    ### Arguments:

    - `controller`      - defines which krita property will be modified
    - `values_to_cycle` - list or range of values to switch to
                           compatibile with controller
    - `default_value`   - value to switch to when current value is not in the
                           list. It has to belong to the list.
    - `sensitivity`     - how much movement is needed to switch values

    ### Usage Example:

    Slider example allows to pick one of 5 presets defined using their
    name. If active preset does not belong to the list, the tracking
    will start from `b) Basic-1`.
    ```python
    Slider(
            controller=controllers.PresetController(),
            default_value="b) Basic-1",
            values_to_cycle=[
                "a) Eraser Soft",
                "b) Airbrush Soft",
                "b) Basic-1",
                "b) Basic-2 Opacity",
                "b) Basic-3 Flow",
            ]
    )
    ```

    Slider example allows to change painting flow to any value from 10%
    to 100%.
    ```python
    Slider(
            controller=controllers.FlowController(),
            default_value=100,
            values_to_cycle=Range(10, 100)
    )
    ```
    """

    def __init__(
        self,
        controller: Controller,
        values_to_cycle: Union[List[Any], Range],
        default_value: Any,
        sensitivity: int = 50
    ):
        self.__controller = controller
        self.__default_value = default_value
        self.__to_cycle = create_slider_values(
            values_to_cycle,
            self.__default_value)
        self.__sensitivity = sensitivity
        self.__working = False

        self.__instructions: InstructionHolder
        self.__interpreter: MouseInterpreter

    def set_instructions(self, instructions: InstructionHolder) -> None:
        self.__instructions = instructions

    def start(self, mouse_getter: Callable[[], int]) -> None:
        self.__working = True
        self.__interpreter = MouseInterpreter(
            min=self.__to_cycle.min,
            max=self.__to_cycle.max,
            mouse_origin=mouse_getter(),
            start_value=self.__get_current_value(),
            sensitivity=self.__sensitivity,
        )
        Thread(target=self._loop, args=[mouse_getter], daemon=True).start()

    def stop(self):
        self.__working = False

    def _loop(self, mouse_getter: Callable[[], int]) -> None:
        while self.__working:
            self._handle(mouse_getter())
            self.__instructions.update()
            sleep(0.05)

    def _handle(self, mouse: int) -> None:
        clipped_value = self.__interpreter.mouse_to_value(mouse)
        to_set = self.__to_cycle.at(clipped_value)
        self.__controller.set_value(to_set)

    def __get_current_value(self) -> Any:
        try:
            return self.__to_cycle.index(self.__controller.get_value())
        except ValueError:
            return self.__to_cycle.default_value
