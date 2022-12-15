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

    # Arguments:

    - `controller`     -- defines which krita property will be modified
    - `values`         -- list or range of values to switch to
                          compatibile with controller
    - `pixels_in_unit` -- (optional) how many pixels mouse needs to be
                          moved, to change the value by 1.0
    - `deadzone`       -- (optional) amount of pixels a mouse needs to
                          moved for slider to start work
    - `fps_limit`      -- (optional) maximum rate of slider refresh.
                          0 for no limit.

    # Usage Example:

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
    )
    ```
    """

    def __init__(
        self,
        controller: Controller,
        values: Union[List[Any], Range],
        pixels_in_unit: Optional[int] = None,
        deadzone: Optional[int] = None,
        fps_limit: Optional[int] = None
    ) -> None:
        self.controller = controller
        self.values = values
        self.pixels_in_unit = self._read(pixels_in_unit, Config.PIXELS_IN_UNIT)
        self.deadzone = self._read(deadzone, Config.SLIDER_DEADZONE)
        self.fps_limit = self._read(fps_limit, Config.FPS_LIMIT)
        self.sleep_time = 1/self.fps_limit if self.fps_limit else 0.001

    def _read(self, passed: Optional[int], field: Config):
        if passed is not None:
            return passed
        return field.get()
