# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, TypeVar, Generic, Optional
from enum import Enum

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from core_components import Controller, Instruction
from input_adapter import ComplexAction
from .pie_menu_utils import (
    create_pie_settings_window,
    create_local_config,
    PieManager,
    PieWidget,
    PieStyle,
    Label)
from .pie_menu_utils.widget_utils import EditMode, RoundButton, NotifyingList

T = TypeVar('T')


class PieMenu(ComplexAction, Generic[T]):
    """
    Pick value by hovering over a pie menu widget.

    - Widget is displayed under the cursor between key press and release
    - Moving mouse in a direction of a value activates in on key release
    - When the mouse was not moved past deadzone, value is not changed
    - Dragging values activates edit mode in which pie does not hide
    - Applying the changes in edit mode, saves its values to settings

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `values`        -- list of values compatibile with controller to cycle
    - `instructions`  -- (optional) list of additional instructions to
                         perform on key press and release
    - `pie_radius_scale`  -- (optional) widget size multiplier
    - `icon_radius_scale` -- (optional) icons size multiplier
    - `background_color`  -- (optional) rgba color of background
    - `active_color`      -- (optional) rgba color of active pie
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long

    ### Action implementation example:

    Action is meant to change opacity of current layer to one of
    predefined values using the pie menu widget.


    ```python
    templates.PieMenu(
        name="Pick active layer opacity",
        controller=controllers.LayerOpacityController(),
        values=[100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
        pie_radius_scale=1.3   # 30% larger menu
        icon_radius_scale=0.9  # 10% smaller icons
        background_color=QColor(255, 0, 0, 128)  # 50% red
        active_color=QColor(0, 0, 255)           # 100% blue
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
    - Setting a value on key release when the deadzone was reached
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: List[T],
        instructions: List[Instruction] = [],
        pie_radius_scale: float = 1.0,
        icon_radius_scale: float = 1.0,
        background_color: Optional[QColor] = None,
        active_color: QColor = QColor(100, 150, 230, 255),
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(
            name=name,
            short_vs_long_press_time=short_vs_long_press_time,
            instructions=instructions)
        self._controller = controller
        self._local_config = create_local_config(
            name,
            values,
            pie_radius_scale,
            icon_radius_scale)

        # TODO: colors should be in self._local_config
        self._background_color = background_color
        self._active_color = active_color

        self._labels: NotifyingList[Label] = NotifyingList()
        self._all_labels: NotifyingList[Label] = NotifyingList()
        self._reset_labels(self._all_labels, self._get_all_values(values))

        self._edit_mode = EditMode(self)

        self._unscaled_style = PieStyle(
            pie_radius_scale=self._local_config.pie_radius_scale,
            icon_radius_scale=self._local_config.icon_radius_scale,
            background_color=self._background_color,
            active_color=self._active_color,
            items=[None])
        self._style = PieStyle(
            pie_radius_scale=self._local_config.pie_radius_scale,
            icon_radius_scale=self._local_config.icon_radius_scale,
            background_color=self._background_color,
            active_color=self._active_color,
            items=self._labels)

        self.pie_settings = create_pie_settings_window(
            style=self._unscaled_style,
            values=self._all_labels,
            used_values=self._labels,
            pie_config=self._local_config)
        self.pie_widget = PieWidget(
            style=self._style,
            labels=self._labels,
            config=self._local_config)
        self.pie_manager = PieManager(
            pie_widget=self.pie_widget,
            pie_settings=self.pie_settings)

        self.settings_button = RoundButton(
            icon=Krita.get_icon("properties"),
            parent=self.pie_widget)
        self.settings_button.clicked.connect(lambda: self._edit_mode.set(True))
        self.accept_button = RoundButton(
            icon=Krita.get_icon("dialog-ok"),
            parent=self.pie_widget)
        self.accept_button.clicked.connect(lambda: self._edit_mode.set(False))
        self.accept_button.hide()

    def reset(self):
        values = self._local_config.values
        self._reset_labels(self._labels, values)

        self.pie_widget.reset(self._style)
        self.pie_settings.reset(self._unscaled_style)

        default_radius = self._style.setting_button_radius
        radius = self._style.deadzone_radius
        radius = int(radius) if radius != float("inf") else default_radius

        self.settings_button.reset(
            radius=default_radius,
            icon_scale=1.1,
            style=self._style)
        self.settings_button.move(QPoint(
            self.pie_widget.width()-self.settings_button.width(),
            self.pie_widget.height()-self.settings_button.height()))

        self.accept_button.reset(
            radius=radius,
            icon_scale=1.5,
            style=self._style)
        self.accept_button.move_center(self.pie_widget.center)

    def on_key_press(self) -> None:
        """Show widget under mouse and start manager which repaints it."""
        self._controller.refresh()
        self.reset()
        self.pie_manager.start()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        """Stop the widget. Set selected value if deadzone was reached."""
        super().on_every_key_release()
        if self._edit_mode.get():
            return

        self.pie_manager.stop()
        self.pie_widget.hide()
        if label := self.pie_widget.active:
            self._controller.set_value(label.value)

    def _reset_labels(self, label_list: List[Label[T]], values: List[T]):
        """Wrap values into paintable label objects with position info."""
        current = [label.value for label in label_list]
        if current == values:
            return

        label_list.clear()
        for value in values:
            try:
                label = self._controller.get_label(value)
            except KeyError:
                continue
            label_list.append(Label(value=value, display_value=label))

    def _get_all_values(self, values: List[T]) -> List[T]:
        if not values:
            return []

        value_type = values[0]
        if not isinstance(value_type, Enum):
            return []

        names = type(value_type)._member_names_
        return [type(value_type)[name] for name in names]
