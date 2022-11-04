from dataclasses import dataclass, field
from threading import Thread
from time import sleep
from typing import List, Literal, Optional

from ..api import Krita
from ..connection_utils import PluginAction
from ..components import Instruction, InstructionHolder
from .slider_utils import Slider


class MouseTracker:
    def __new__(
        cls,
        action_name: str,
        horizontal_slider: Optional[Slider] = None,
        vertical_slider: Optional[Slider] = None,
        instructions: List[Instruction] = [],
    ) -> PluginAction:
        if horizontal_slider and not vertical_slider:
            return SingleAxisTracker(
                action_name=action_name,
                slider=horizontal_slider,
                instructions=InstructionHolder(instructions),
                sign=1
            )
        if not horizontal_slider and vertical_slider:
            return SingleAxisTracker(
                action_name=action_name,
                slider=vertical_slider,
                instructions=InstructionHolder(instructions),
                sign=-1
            )
        if horizontal_slider and vertical_slider:
            return DoubleAxisTracker(
                action_name=action_name,
                horizontal_slider=horizontal_slider,
                vertical_slider=vertical_slider,
                instructions=InstructionHolder(instructions)
            )
        raise ValueError("At least one slider needed.")


@dataclass
class SingleAxisTracker(PluginAction):
    action_name: str
    slider: Slider
    instructions: InstructionHolder
    sign: Literal[1, -1] = 1

    _time_interval = 0.1
    _working = False

    def __post_init__(self):
        self.slider.set_instructions(self.instructions)

    def on_key_press(self) -> None:
        self.instructions.enter()
        cursor = Krita.get_cursor()
        return self.slider.start(lambda: self.sign*cursor.y())

    def on_every_key_release(self) -> None:
        self.slider.stop()
        self.instructions.exit()


@dataclass
class DoubleAxisTracker(PluginAction):
    action_name: str
    horizontal_slider: Slider
    vertical_slider: Slider
    instructions: InstructionHolder = field(default_factory=list)

    _time_interval = 0.1
    _working = False

    def __post_init__(self):
        self.horizontal_slider.set_instructions(self.instructions)
        self.vertical_slider.set_instructions(self.instructions)

    def on_key_press(self) -> None:
        self.instructions.enter()
        Thread(target=self._pick_slider, daemon=True).start()

    def _pick_slider(self) -> None:
        cursor = Krita.get_cursor()
        start_point = (cursor.x(), cursor.y())
        while True:
            delta_hor = abs(start_point[0] - cursor.x())
            delta_ver = abs(start_point[1] - cursor.y())
            if abs(delta_hor - delta_ver) >= 10:
                break
            sleep(0.05)

        if delta_hor > delta_ver:
            self.horizontal_slider.start(cursor.x)
        else:
            self.vertical_slider.start(lambda: -cursor.y())

    def on_every_key_release(self) -> None:
        self.horizontal_slider.stop()
        self.vertical_slider.stop()
        self.instructions.exit()
