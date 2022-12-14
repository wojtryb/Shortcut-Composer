from typing import List, TypeVar, Generic, Union

from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtCore import QPoint

from shortcut_composer_config import (
    SHORT_VS_LONG_PRESS_TIME,
    PIE_BACKGROUND_COLOR,
    PIE_ACTIVE_COLOR,
)
from core_components import Controller, Instruction
from input_adapter import PluginAction
from api_krita.pyqt import Text
from .pie_menu_utils import (
    AngleCalculator,
    LabelHolder,
    PieManager,
    PieWidget,
    PieStyle,
    Label,
)

T = TypeVar('T')


class PieMenu(PluginAction, Generic[T]):
    """
    Pick value by hovering over a pie menu widget.

    - Widget is displayed under the cursor between key press and release
    - Moving mouse in a direction of a value activates in on key release
    - When the mouse was not moved past deadzone, value is not changed

    # Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `values`        -- list of values compatibile with controller to cycle
    - `instructions`  -- (optional) list of additional instructions to
                         perform on key press and release
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long
    - `pie_radius_scale`  -- (optional) widget size multiplier
    - `icon_radius_scale` -- (optional) icons size multiplier
    - `background_color`  -- (optional) rgba color of background
    - `active_color`      -- (optional) rgba color of active pie

    # Action implementation example:

    Action is meant to change opacity of current layer to one of
    predefined values using the pie menu widget.


    ```python
    templates.PieMenu(
        name="Pick active layer opacity",
        controller=controllers.LayerOpacityController(),
        values=[100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
    )
    ```
    """
    """
    Class is responsible for:
    - Handling the key press/release interface
    - Reading widget configuration and storing it in PieStyle - passed
      to objects that can be displayed
    - Creating the PieWidget - and PieManager which displays it
    - Starting and stopping the PieManager on key press and release
    - Creating Labels - paintable representations of handled values
    - Storing created labels in LabelHolder which allows to fetch them
      by the angle on a pie
    - Setting a value on key release when the deadzone was reached
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller,
        values: List[T],
        instructions: List[Instruction] = [],
        short_vs_long_press_time: float = SHORT_VS_LONG_PRESS_TIME,
        pie_radius_scale: float = 1.0,
        icon_radius_scale: float = 1.0,
        background_color: QColor = PIE_BACKGROUND_COLOR,
        active_color: QColor = PIE_ACTIVE_COLOR,
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller

        self._style = PieStyle(
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            background_color=background_color,
            active_color=active_color,
        )
        self._labels = self._create_labels(values)
        self._style.adapt_to_item_amount(len(self._labels))

        self._pie_manager = PieManager(PieWidget(self._labels, self._style))

    def on_key_press(self) -> None:
        """Show widget under mouse and start manager which repaints it."""
        self._controller.refresh()
        self._pie_manager.start()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        """Stop the widget. Set selected value if deadzone was reached."""
        super().on_every_key_release()
        self._pie_manager.stop()
        if label := self._labels.active:
            self._controller.set_value(label.value)

    def _create_labels(self, values: List[T]) -> LabelHolder:
        """Wrap values into paintable label objects with position info."""
        label_list = []
        for value in values:
            if icon := self._get_icon_if_possible(value):
                label_list.append(Label(value=value, display_value=icon))

        center = QPoint(self._style.widget_radius, self._style.widget_radius)
        angle_calculator = AngleCalculator(
            center=center,
            radius=self._style.pie_radius)
        angle_iterator = angle_calculator.iterate_over_circle(len(label_list))

        label_holder = LabelHolder()
        for label, (angle, point) in zip(label_list, angle_iterator):
            label.angle = angle
            label.center = point
            label_holder.add(label)

        return label_holder

    def _get_icon_if_possible(self, value: T) -> Union[Text, QPixmap, None]:
        """Return the paintable icon of the value or None if missing."""
        try:
            return self._controller.get_label(value)
        except KeyError:
            return None
