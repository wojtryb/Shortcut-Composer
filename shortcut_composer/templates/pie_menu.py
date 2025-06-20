# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable
from functools import cached_property

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.pyqt import RoundButton
from data_components import PieDeadzoneStrategy
from composer_utils import Config
from core_components import Controller, Instruction
from .pie_menu_utils.group_manager_impl import dispatch_group_manager
from .pie_menu_utils import PieConfig
from .pie_menu_utils import (
    PieCurrentValueHolder,
    PieEditModeHandler,
    PieMouseTracker,
    PieStyleHolder,
    PieActuator,
    PieSettings,
    PieWidget)
from .raw_instructions import RawInstructions

T = TypeVar('T')


class PieMenu(RawInstructions, Generic[T]):
    """
    Pick value by hovering over a pie menu widget.

    - Widget is displayed under the cursor between key press and release
    - Moving mouse in a direction of a value activates it on key release
    - When in deadzone, selected strategy is used to determine action
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
    - `pie_opacity`       -- (optional) default opacity of the pie
    - `save_local`        -- (optional) default save location
    - `deadzone_strategy` -- (optional) default strategy what to do,
                              when mouse does not leave deadzone
    - `max_lines_amount`  -- (optional) default limit of lines of text
    - `max_signs_amount`  -- (optional) default limit of signs in line
    - `abbreviate_with_dot` -- (optional) whether '.' sign should be
                               used for abbreviating words
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
        pie_radius_scale=1.3                     # 30% larger menu
        icon_radius_scale=0.9                    # 10% smaller icons
        background_color=QColor(255, 0, 0, 128)  # 50% red
        active_color=QColor(0, 0, 255)           # 100% blue
    )
    ```
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: list[T],
        instructions: list[Instruction] | None = None,
        pie_radius_scale: float = 1.0,
        icon_radius_scale: float = 1.0,
        background_color: QColor | None = None,
        active_color: QColor | None = None,
        pie_opacity: int = 75,
        save_local: bool = False,
        deadzone_strategy=PieDeadzoneStrategy.DO_NOTHING,
        max_lines_amount: int = 2,
        max_signs_amount: int = 8,
        abbreviate_with_dot: bool = True,
        short_vs_long_press_time: float | None = None
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller

        self._config = PieConfig(
            name=f"ShortcutComposer: {name}",
            values=values,
            controller=controller,
            pie_radius_scale=pie_radius_scale,
            icon_radius_scale=icon_radius_scale,
            save_local=save_local,
            background_color=background_color,
            active_color=active_color,
            pie_opacity=pie_opacity,
            deadzone_strategy=deadzone_strategy,
            max_lines_amount=max_lines_amount,
            max_signs_amount=max_signs_amount,
            abbreviate_with_dot=abbreviate_with_dot)

        self._edit_mode_handler = PieEditModeHandler(self)
        self._style_holder = PieStyleHolder(self._config)
        self._label_creator = dispatch_group_manager(self._controller)
        self._actuator = PieActuator(
            controller=self._controller,
            strategy_field=self._config.DEADZONE_STRATEGY)

        # Usually, when labels stay same, recreating widgets is not needed.
        # When widget scale changes, they have to be reloaded.
        def raise_flag():
            self._force_reload = True
        self._force_reload = False
        self._register_callback_to_size_change(raise_flag)

    @cached_property
    def pie_widget(self) -> PieWidget:
        """Create Qwidget of the Pie for selecting values."""
        pie_widget = PieWidget(
            pie_style=self._style_holder.pie_style,
            allowed_types=self._controller.TYPE,
            allow_value_edit_callback=lambda: not self._config.TAG_MODE.read())

        # This is the first `settings_button` occurence, which creates it
        self.settings_button.setParent(pie_widget)

        self._register_callback_to_size_change(pie_widget.reset_size)
        return pie_widget

    @cached_property
    def pie_settings(self) -> PieSettings:
        """Create QWidget with pie settings right for given type of labels."""
        return PieSettings(
            config=self._config,
            style_holder=self._style_holder,  # TODO: pass just label_style?
            controller=self._controller,
            order_handler=self.pie_widget.order_handler)

    @cached_property
    def pie_mouse_tracker(self) -> PieMouseTracker:
        """Create Manager which shows, hides and moves the Pie."""
        return PieMouseTracker(self.pie_widget)

    @cached_property
    def settings_button(self) -> RoundButton:
        """Create button with which user can enter the edit mode."""
        pie_style = self._style_holder.pie_style

        settings_button = RoundButton(
            radius_callback=lambda: pie_style.setting_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("properties"),
            icon_scale=1.1)
        settings_button.clicked.connect(
            self._edit_mode_handler.set_edit_mode_true)

        def move_to_bottom_left():
            pie_size = 2*self._style_holder.pie_style.widget_radius
            button_size = 2*self._style_holder.small_label_style.icon_radius
            position = pie_size-button_size
            settings_button.move(QPoint(position, position))
        self._register_callback_to_size_change(move_to_bottom_left)
        move_to_bottom_left()

        return settings_button

    @cached_property
    def accept_button(self) -> RoundButton:
        """Create button displayed in edit mode, for hiding the pie."""
        pie_style = self._style_holder.pie_style

        accept_button = RoundButton(
            radius_callback=lambda: pie_style.accept_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("dialog-ok"),
            icon_scale=1.5,
            parent=self.pie_widget)

        def on_click():
            self._edit_mode_handler.set_edit_mode_false()
            values = [label.value for label in self.pie_widget.order_handler]
            self._config.set_values(values)
        accept_button.clicked.connect(on_click)
        accept_button.hide()

        def move_to_pie_center():
            radius = self._style_holder.pie_style.widget_radius
            accept_button.move_center(QPoint(radius, radius))
        self._register_callback_to_size_change(move_to_pie_center)
        move_to_pie_center()

        return accept_button

    @cached_property
    def current_value_holder(self) -> PieCurrentValueHolder:
        """Create a LabelWidget holder with currently selected value."""
        value_holder = PieCurrentValueHolder(
            self._controller,
            self._style_holder.small_label_style,
            self.pie_widget)

        def move_to_bottom_left():
            pie_size = 2*self._style_holder.pie_style.widget_radius
            button_size = 2*self._style_holder.small_label_style.icon_radius
            position = pie_size-button_size
            value_holder.move(QPoint(position, position))
        self._register_callback_to_size_change(move_to_bottom_left)
        move_to_bottom_left()

        return value_holder

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()

        # This is the first `pie_widget` occurence, which creates it
        if self.pie_widget.isVisible():
            return

        new_labels = self._label_creator.create_labels(self._config.values())
        current_labels = self.pie_widget.order_handler.labels

        if new_labels != current_labels or self._force_reload:
            self._force_reload = False
            self.pie_widget.order_handler.replace_labels(new_labels)

        self.current_value_holder.refresh()
        self._actuator.mark_selected_widget(self.pie_widget.order_handler)

        self.pie_mouse_tracker.start()

    def on_every_key_release(self) -> None:
        """
        Handle the key release event.

        In normal mode:
            Close pie, and set selected value if deadzone was reached.
        In edit mode:
            Ignore input.
        """
        super().on_every_key_release()

        if self._edit_mode_handler.is_in_edit_mode:
            return

        # Hide the widget before label gets activated
        # Activation can open windows, which is better whth pie hidden
        self.pie_widget.hide()
        self._actuator.activate(
            self.pie_widget.active_label,
            self.pie_widget.order_handler.labels)
        self.pie_mouse_tracker.stop()

    def _register_callback_to_size_change(self, callback: Callable[[], None]):
        self._config.PIE_RADIUS_SCALE.register_callback(callback)
        self._config.ICON_RADIUS_SCALE.register_callback(callback)
        Config.PIE_GLOBAL_SCALE.register_callback(callback)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(callback)
