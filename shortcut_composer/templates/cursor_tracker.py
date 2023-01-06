# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from core_components import Instruction
from data_components import Slider
from input_adapter import ComplexAction
from .mouse_tracker_utils import (
    SingleAxisTracker,
    DoubleAxisTracker,
    SliderHandler,
)


class CursorTracker(ComplexAction):
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
                             in shortcut_composer.action file.
    - `horizontal_slider` -- (optional*) defines what to do on horizontal
                             mouse movement.
    - `vertical_slider`   -- (optional*) defines what to do on vertical
                             mouse movement.
    - `instructions`      -- (optional) list of additional instructions
                             to perform on key press, release and during
                             key being pressed.

    *providing at least one of sliders is required.

    ### Action implementation examples:

    Exaples of defining a tracker for one, and for both axes.

    ```python
    templates.CursorTracker(
        name="Horizontal axis tracker",
        horizontal_slider=Slider(...), # See `Slider`
    )
    templates.CursorTracker(
        name="Double axis tracker",
        horizontal_slider=Slider(...), # See `Slider`
        vertical_slider=Slider(...),   # See `Slider`
    )
    ```
    """

    def __new__(
        cls,
        name: str,
        horizontal_slider: Optional[Slider] = None,
        vertical_slider: Optional[Slider] = None,
        instructions: List[Instruction] = [],
    ) -> ComplexAction:
        """
        Pick and create correct ActionPlugin based on provided sliders.

        Horizontal slider requires SingleAxisTracker.
        Vertical slider requires SingleAxisTracker with negated axis.
        Both sliders require DoubleAxisTracker.
        """
        if horizontal_slider and not vertical_slider:
            return SingleAxisTracker(
                name=name,
                instructions=instructions,
                slider_handler=SliderHandler(
                    slider=horizontal_slider,
                    is_horizontal=True,
                )
            )
        if not horizontal_slider and vertical_slider:
            return SingleAxisTracker(
                name=name,
                instructions=instructions,
                slider_handler=SliderHandler(
                    slider=vertical_slider,
                    is_horizontal=False,
                )
            )
        if horizontal_slider and vertical_slider:
            return DoubleAxisTracker(
                name=name,
                instructions=instructions,
                horizontal_handler=SliderHandler(
                    slider=horizontal_slider,
                    is_horizontal=True,
                ),
                vertical_handler=SliderHandler(
                    slider=vertical_slider,
                    is_horizontal=False,
                )
            )
        raise ValueError("At least one slider needed.")

    def __init__(
        self,
        name: str,
        horizontal_slider: Optional[Slider] = None,
        vertical_slider: Optional[Slider] = None,
        instructions: List[Instruction] = [],
    ) -> None: ...
