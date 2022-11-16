from typing import List, Optional

from input_adapter import PluginAction
from core_components import Instruction
from data_components import Slider
from .mouse_tracker_utils import (
    SingleAxisTracker,
    DoubleAxisTracker,
    SliderHandler,
)


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

    - `name`              -- unique name of action. Must match the definition
                              in shortcut_composer.action file
    - `horizontal_slider` -- defines what to do on horizontal mouse movement
    - `vertical_slider`   -- defines what to do on vertical mouse movement
    - `instructions`      -- list of additional instructions to perform on
                              key press, release and during key being pressed.

    ### Action implementation examples:

    ```python
    MouseTracker(
        name="Horizontal axis tracker",
        horizontal_slider=Slider(...), # See slider documentation
    )
    MouseTracker(
        name="Double axis tracker",
        horizontal_slider=Slider(...),
        vertical_slider=Slider(...),
    )
    ```
    """
    def __new__(
        cls,
        name: str,
        horizontal_slider: Optional[Slider] = None,
        vertical_slider: Optional[Slider] = None,
        instructions: List[Instruction] = [],
        deadzone: int = 10,
    ) -> PluginAction:
        """
        Pick and create correct tracker based on provided sliders.

        Horizontal slider requires SingleAxisTracker.
        Vertical slider requires SingleAxisTracker with negated axis.
        Both sliders require DoubleAxisTracker.
        """
        if horizontal_slider and not vertical_slider:
            return SingleAxisTracker(
                name=name,
                is_horizontal=True,
                instructions=instructions,
                handler=SliderHandler(horizontal_slider),
                deadzone=deadzone
            )
        if not horizontal_slider and vertical_slider:
            return SingleAxisTracker(
                name=name,
                is_horizontal=False,
                instructions=instructions,
                handler=SliderHandler(vertical_slider),
                deadzone=deadzone
            )
        if horizontal_slider and vertical_slider:
            return DoubleAxisTracker(
                name=name,
                instructions=instructions,
                horizontal_handler=SliderHandler(horizontal_slider),
                vertical_handler=SliderHandler(vertical_slider),
                deadzone=deadzone
            )
        raise ValueError("At least one slider needed.")
