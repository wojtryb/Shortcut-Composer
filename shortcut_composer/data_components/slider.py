from typing import Any, List, Union, Optional

from composer_utils import Config
from core_components import Controller
from .range import Range


class Slider:
    """
    Part of MouseTracker specifying what to do on single axis movement.

    While the slider is active the value is being changed relatively to
    the offset from the starting value.

    The `slider_values` can be either:
    -  a discrete list of values
    -  a contiguous range defined using Range(start, stop)

    ### Arguments:

    - `controller`        -- defines which krita property will be modified
    - `values`            -- list or range of values to switch to
                             compatibile with controller
    - `sensitivity_scale` -- (optional) changes sensitivity of slider
    - `deadzone`          -- (optional) amount of pixels a mouse needs
                             to be moved for slider to start to work

    ### Usage Example:

    Slider example allows to pick one of 5 presets defined using their
    name. If active preset does not belong to the list, the tracking
    will start from `b) Basic-1`.
    ```python
    Slider(
            controller=controllers.PresetController(),
            values=[
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
            values=Range(10, 100)
            sensitivity_scale=2  # slider is 2x more sensitive than others
            deadzone=20          # move 20 pixels to start sliding
    )
    ```
    """

    def __init__(
        self,
        controller: Controller,
        values: Union[List[Any], Range],
        sensitivity_scale: float = 1.0,
        deadzone: Optional[int] = None,
    ) -> None:
        self.controller = controller
        self.values = values

        sensitivity = Config.SLIDER_SENSITIVITY_SCALE.read()*sensitivity_scale
        self.pixels_in_unit = round(50 / sensitivity)

        self.deadzone = self._read(deadzone, Config.SLIDER_DEADZONE)

    def _read(self, passed: Optional[int], field: Config) -> int:
        if passed is not None:
            return passed
        return field.read()
