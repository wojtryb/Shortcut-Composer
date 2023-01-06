from typing import Any, List, Union
from dataclasses import dataclass

from core_components import Controller
from .range import Range


@dataclass
class Slider:
    """
    Part of MouseTracker specifying what to do on single axis movement.

    While the slider is active the value is being changed relatively to
    the offset from the starting value.

    The `slider_values` can be either:
    -  a discrete list of values
    -  a contiguous range defined using Range(start, stop)

    ### Arguments:

    - `controller`      - defines which krita property will be modified
    - `slider_values` - list or range of values to switch to
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
    controller: Controller
    values: Union[List[Any], Range]
    sensitivity: int = 50
