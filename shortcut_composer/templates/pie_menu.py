# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, TypeVar, Generic, Optional
from functools import cached_property

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from composer_utils.label import Label
from data_components import DeadzoneStrategy
from core_components import Controller, Instruction
from .pie_menu_utils.pie_config_impl import dispatch_pie_config
from .pie_menu_utils.pie_settings_impl import dispatch_pie_settings
from .pie_menu_utils import (
    StyleManager,
    PieSettings,
    PieManager,
    PieWidget,
    PieButton,
    Actuator,
    EditMode)
from .raw_instructions import RawInstructions

T = TypeVar('T')


class PieMenu(RawInstructions, Generic[T]):
    """
    Pick value by hovering over a pie menu widget.

    - Widget is displayed under the cursor between key press and release
    - Moving mouse in a direction of a value activates it on key release
    - When the mouse was not moved past deadzone, value is not changed
    - Edit button activates mode in which pie does not hide on key
      release and can be configured (see PieSettings)

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `values`        -- default list of values to display in pie
    - `instructions`  -- (optional) list of additional instructions to
                         perform on key press and release
    - `pie_radius_scale`  -- (optional) default widget size multiplier
    - `icon_radius_scale` -- (optional) default icons size multiplier
    - `background_color`  -- (optional) default rgba color of background
    - `active_color`      -- (optional) default rgba color of active pie
    - `pie opacity`       -- (optional) default opacity of the pie
    - `save local`        -- (optional) default save location
    - `deadzone strategy` -- (optional) default strategy what to do,
                              when mouse does not leave deadzone
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
        active_color: Optional[QColor] = None,
        pie_opacity: int = 75,
        save_local: bool = False,
        deadzone_strategy: DeadzoneStrategy = DeadzoneStrategy.DO_NOTHING,
        short_vs_long_press_time: Optional[float] = None
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller

        self._config = dispatch_pie_config(self._controller)(
            name=f"ShortcutComposer: {name}",
            values=values,
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            save_local=save_local,
            background_color=background_color,
            active_color=active_color,
            pie_opacity=pie_opacity,
            deadzone_strategy=deadzone_strategy)
        self._config.ORDER.register_callback(self._reset_labels)

        self._labels: List[Label] = []
        self._edit_mode = EditMode(self)
        self._style_manager = StyleManager(pie_config=self._config)
        self.actuator = Actuator(
            controller=self._controller,
            strategy_field=self._config.DEADZONE_STRATEGY,
            labels=self._labels)

    @cached_property
    def pie_widget(self) -> PieWidget:
        """Create Qwidget of the Pie for selecting values."""
        return PieWidget(
            pie_style=self._style_manager.pie_style,
            labels=self._labels,
            edit_mode=self._edit_mode,
            config=self._config)

    @cached_property
    def pie_settings(self) -> PieSettings:
        """Create QWidget with pie settings right for given type of labels."""
        return dispatch_pie_settings(self._controller)(
            config=self._config,
            pie_style=self._style_manager.pie_style,
            controller=self._controller)

    @cached_property
    def pie_manager(self) -> PieManager:
        """Create Manager which shows, hides and moves the Pie."""
        return PieManager(pie_widget=self.pie_widget)

    @cached_property
    def settings_button(self):
        """Create button with which user can enter the edit mode."""
        settings_button = PieButton(
            icon=Krita.get_icon("properties"),
            icon_scale=1.1,
            parent=self.pie_widget,
            radius_callback=lambda: self._style_manager.pie_style
            .setting_button_radius,
            pie_style=self._style_manager.pie_style,
            config=self._config)
        settings_button.clicked.connect(lambda: self._edit_mode.set(True))
        return settings_button

    @cached_property
    def accept_button(self):
        """Create button displayed in edit mode, for hiding the pie."""
        accept_button = PieButton(
            icon=Krita.get_icon("dialog-ok"),
            icon_scale=1.5,
            parent=self.pie_widget,
            radius_callback=lambda: self._style_manager.pie_style
            .accept_button_radius,
            pie_style=self._style_manager.pie_style,
            config=self._config)

        # Work around the Qt bug where button resets to (0, 0) on config change
        self._config.register_callback(self._move_accept_button_to_center)

        accept_button.clicked.connect(lambda: self._edit_mode.set(False))
        accept_button.hide()
        return accept_button

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()

        if self.pie_widget.isVisible():
            return

        self._controller.refresh()
        self._reset_labels()
        self.pie_widget.label_holder.reset()  # HACK: should be automatic
        self._move_accept_button_to_center()
        self.settings_button.move(QPoint(
            self.pie_widget.width()-self.settings_button.width(),
            self.pie_widget.height()-self.settings_button.height()))
        self.actuator.mark_selected_widget(self.pie_widget.widget_holder)

        self.pie_manager.start()

    INVALID_VALUES: 'set[T]' = set()

    def _reset_labels(self) -> None:
        """Replace list values with newly created labels."""
        values = self._config.values()

        # Workaround of krita tags sometimes returning invalid presets
        # Bad values are remembered in class attribute and filtered out
        filtered_values = [v for v in values if v not in self.INVALID_VALUES]
        current_values = [label.value for label in self._labels]

        # Method is expensive, and should not be performed when values
        # did not in fact change.
        if filtered_values == current_values:
            return

        self._labels.clear()
        for value in values:
            label = Label.from_value(value, self._controller)
            if label is not None:
                self._labels.append(label)
            else:
                self.INVALID_VALUES.add(value)

        self._config.refresh_order()

    def on_every_key_release(self) -> None:
        """
        Handle the key release event.

        In normal mode:
            close pie, and set selected value if deadzone was reached
        In edit mode:
            ignore input

        """
        super().on_every_key_release()

        if self._edit_mode:
            return

        self.actuator.activate(self.pie_widget.active)
        self.pie_manager.stop()

    def _move_accept_button_to_center(self):
        """Ensure the accept button is in the center of the pie."""
        self.accept_button.move_center(self.pie_widget.center)
