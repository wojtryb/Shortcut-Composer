# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, TypeVar, Generic, Optional

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from core_components import Controller, Instruction
from .pie_menu_utils import (
    create_pie_settings_window,
    create_local_config,
    PieManager,
    PieWidget,
    PieStyle,
    Label)
from .pie_menu_utils.widget_utils import EditMode, PieButton
from .raw_instructions import RawInstructions

T = TypeVar('T')


class PieMenu(RawInstructions, Generic[T]):
    """
    Pick value by hovering over a pie menu widget.

    - Widget is displayed under the cursor between key press and release
    - Moving mouse in a direction of a value activates in on key release
    - When the mouse was not moved past deadzone, value is not changed
    - Edit button activates mode in pie does not hide and can be changed

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

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: List[T],
        instructions: Optional[List[Instruction]] = None,
        pie_radius_scale: float = 1.0,
        icon_radius_scale: float = 1.0,
        background_color: Optional[QColor] = None,
        active_color: QColor = QColor(100, 150, 230, 255),
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller
        self._config = create_local_config(
            name=name,
            values=values,
            controller_type=self._controller.TYPE,
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            background_color=background_color,
            active_color=active_color)
        self._config.ORDER.register_callback(
            lambda: self._reset_labels(self._config.values()))

        self._last_values: List[T] = []
        self._labels: List[Label] = []
        self._reset_labels(self._config.values())
        self._edit_mode = EditMode(self)
        self._style = PieStyle(items=self._labels, pie_config=self._config)

        self.pie_settings = create_pie_settings_window(
            controller=self._controller,
            style=self._style,
            used_labels=self._labels,
            pie_config=self._config)
        self.pie_widget = PieWidget(
            style=self._style,
            labels=self._labels,
            config=self._config)
        self.pie_manager = PieManager(
            pie_widget=self.pie_widget,
            pie_settings=self.pie_settings)

        self.settings_button = PieButton(
            icon=Krita.get_icon("properties"),
            icon_scale=1.1,
            parent=self.pie_widget,
            radius_callback=lambda: self._style.setting_button_radius,
            style=self._style,
            config=self._config)
        self.settings_button.clicked.connect(lambda: self._edit_mode.set(True))
        self.accept_button = PieButton(
            icon=Krita.get_icon("dialog-ok"),
            icon_scale=1.5,
            parent=self.pie_widget,
            radius_callback=lambda: self._style.accept_button_radius,
            style=self._style,
            config=self._config)
        self.accept_button.clicked.connect(lambda: self._edit_mode.set(False))
        self.accept_button.hide()

    def _move_buttons(self):
        """Move accept button to center and setting button to bottom-right."""
        self.accept_button.move_center(self.pie_widget.center)
        self.settings_button.move(QPoint(
            self.pie_widget.width()-self.settings_button.width(),
            self.pie_widget.height()-self.settings_button.height()))

    def on_key_press(self) -> None:
        """Reload labels, start GUI manager and run instructions."""
        if self.pie_widget.isVisible():
            return

        self._controller.refresh()

        new_values = self._config.values()
        if self._last_values != new_values:
            self._reset_labels(new_values)
            self._last_values = new_values
            self.pie_widget.label_holder.reset()  # HACK: should be automatic

        self._move_buttons()

        self.pie_manager.start()
        super().on_key_press()

    def on_every_key_release(self) -> None:
        """
        Handle the key release event.

        Ignore if in edit mode. Otherwise, stop the manager and set the
        selected value if deadzone was reached.
        """
        super().on_every_key_release()

        if self._edit_mode.get():
            return

        self.pie_manager.stop()
        if label := self.pie_widget.active:
            self._controller.set_value(label.value)

    def _reset_labels(self, values: List[T]) -> None:
        """Replace list values with newly created labels."""
        self._labels.clear()
        for value in values:
            label = Label.from_value(value, self._controller)
            if label is not None:
                self._labels.append(label)
