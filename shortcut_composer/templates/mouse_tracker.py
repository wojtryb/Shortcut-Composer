from dataclasses import dataclass
from threading import Thread, Lock
from time import sleep
from typing import List, Literal, Optional

from api_krita import Krita
from input_adapter import PluginAction
from core_components import Instruction, InstructionHolder
from data_components import Slider
from .mouse_tracker_utils import SliderHandler


class MouseTracker:
    """
    Switch values with horizontal or vertical mouse movement.

    Action tracks mouse during key being pressed, and switches values
    accordingly to mouse movement.

    Class requires providing a Slider in `horizontal_slider` or
    `vertical_slider`. When both are passed, snaps to the axis which has
    the strongest initial movement.

    Providing 'instructions' list allows to add additional logic on key, press,
    release and perform operations in a loop during the key being pressed.

    ### Arguments:

    - `action_name`       -- unique name of action. Must match the definition
                              in shortcut_composer.action file
    - `horizontal_slider` -- defines what to do on horizontal mouse movement
    - `vertical_slider`   -- defines what to do on vertical mouse movement
    - `instructions`      -- list of additional instructions to perform on
                              key press, release and during key being pressed.

    ### Action implementation examples:

    ```python
    MouseTracker(
        action_name="Horizontal axis tracker",
        horizontal_slider=Slider(...), # See slider documentation
    )
    MouseTracker(
        action_name="Double axis tracker",
        horizontal_slider=Slider(...),
        vertical_slider=Slider(...),
    )
    ```
    """
    def __new__(
        cls,
        action_name: str,
        horizontal_slider: Optional[Slider] = None,
        vertical_slider: Optional[Slider] = None,
        instructions: List[Instruction] = [],
    ) -> PluginAction:
        instructions_holder = InstructionHolder(instructions)
        if horizontal_slider and not vertical_slider:
            return SingleAxisTracker(
                action_name=action_name,
                sign=1,
                instructions=instructions_holder,
                handler=SliderHandler(
                    slider=horizontal_slider,
                    instructions=instructions_holder
                ),
            )
        if not horizontal_slider and vertical_slider:
            return SingleAxisTracker(
                action_name=action_name,
                sign=-1,
                instructions=instructions_holder,
                handler=SliderHandler(
                    slider=vertical_slider,
                    instructions=instructions_holder,
                )
            )
        if horizontal_slider and vertical_slider:
            return DoubleAxisTracker(
                action_name=action_name,
                instructions=instructions_holder,
                horizontal_handler=SliderHandler(
                    slider=horizontal_slider,
                    instructions=instructions_holder,
                ),
                vertical_handler=SliderHandler(
                    slider=vertical_slider,
                    instructions=instructions_holder,
                )
            )
        raise ValueError("At least one slider needed.")


@dataclass
class SingleAxisTracker(PluginAction):

    action_name: str
    handler: SliderHandler
    instructions: InstructionHolder
    sign: Literal[1, -1] = 1

    _time_interval = 0.1
    _lock = Lock()

    def on_key_press(self) -> None:
        self._lock.acquire()
        self.instructions.enter()
        cursor = Krita.get_cursor()
        return self.handler.start(lambda: self.sign*cursor.y())

    def on_every_key_release(self) -> None:
        self.handler.stop()
        self.instructions.exit()
        self._lock.release()


@dataclass
class DoubleAxisTracker(PluginAction):

    action_name: str
    horizontal_handler: SliderHandler
    vertical_handler: SliderHandler
    instructions: InstructionHolder

    _time_interval = 0.1
    _lock = Lock()

    def on_key_press(self) -> None:
        Thread(target=self._pick_slider, daemon=True).start()

    def _pick_slider(self) -> None:
        self._lock.acquire()
        self.instructions.enter()
        cursor = Krita.get_cursor()
        start_point = (cursor.x(), cursor.y())
        while True:
            delta_hor = abs(start_point[0] - cursor.x())
            delta_ver = abs(start_point[1] - cursor.y())
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            self.horizontal_handler.start(cursor.x)
        else:
            self.vertical_handler.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        self.horizontal_handler.stop()
        self.vertical_handler.stop()
        self.instructions.exit()
        self._lock.release()
