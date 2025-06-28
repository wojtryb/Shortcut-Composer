# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable
from functools import cached_property

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.pyqt import RoundButton
from composer_utils import Config, GroupOrderHolder
from composer_utils.label.complex_widgets import LabelHolder
from core_components import Controller, Instruction
from data_components import PieDeadzoneStrategy, Tag
from .pie_menu_utils.group_manager_impl import dispatch_group_manager
from .pie_menu_utils import PieConfig
from .pie_menu_utils import (
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

    ### Class design concept
    TODO: programmer guide to this class
    TODO: why cached_property

    When not in edit mode:
    - PieWidget is shown, PieSettings are not
    - labels cannot be dragged
    - settings button is shown. It allows to enter edit mode

    Wnen in edit mode:
    - Both PieWidget and PieSettings are shown
    - labels can be dragged to, from and inside the PieWidget
    - settings button is replaced with current value icon
    - accept button is shown. It allows to hide everything.
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: list[T] | Tag,
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
    ) -> None:
        super().__init__(name, instructions)
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

        self._style_holder = PieStyleHolder(self._config)
        self._label_creator = dispatch_group_manager(self._controller)
        self._group_order_holder = GroupOrderHolder(self._controller.TYPE)

        self._is_in_edit_mode = False
        self._force_reload = False

        # Usually, when labels stay same, recreating widgets is not needed.
        # When widget scale changes, they have to be reloaded.
        def raise_flag():
            self._force_reload = True
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
            style_holder=self._style_holder,
            controller=self._controller,
            order_handler=self.pie_widget.order_handler)

    @cached_property
    def pie_mouse_tracker(self) -> PieMouseTracker:
        """Create Manager which shows, hides and moves the Pie."""
        return PieMouseTracker(self.pie_widget)

    @cached_property
    def pie_actuator(self) -> PieActuator:
        last_value = self._config.LAST_VALUE_SELECTED.read()
        labels = self._label_creator.labels_from_values((last_value,))
        label = labels[0] if labels else None

        pie_actuator = PieActuator(self.pie_widget, label)

        def update_strategy() -> None:
            pie_actuator.strategy = self._config.DEADZONE_STRATEGY.read()
        self._config.DEADZONE_STRATEGY.register_callback(update_strategy)
        update_strategy()

        return pie_actuator

    @cached_property
    def settings_button(self) -> RoundButton:
        """Create button with which user can enter the edit mode."""
        pie_style = self._style_holder.pie_style

        settings_button = RoundButton(
            radius_callback=lambda: self._style_holder.settings_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("properties"),
            icon_scale=1.1)

        def set_edit_mode_on() -> None:
            self.pie_mouse_tracker.stop()

            self.pie_widget.set_draggable(True)
            self.pie_actuator.unmark_all_widgets()
            self.pie_widget.active_label = None
            self.pie_widget.repaint()

            # Move settings next to the pie
            self.pie_settings.show()
            pie_radius = self._style_holder.pie_style.widget_radius
            offset = round(pie_radius + self.pie_settings.width()*0.525)
            center = self.pie_widget.center_global + QPoint(offset, 0)
            self.pie_settings.move_center(center)

            self.accept_button.show()
            self.settings_button.hide()
            self.current_value_holder.show()

            self._is_in_edit_mode = True
        settings_button.clicked.connect(set_edit_mode_on)

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
            radius_callback=lambda: self._style_holder.accept_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("dialog-ok"),
            icon_scale=1.5,
            parent=self.pie_widget)

        def set_edit_mode_off():
            self.pie_widget.hide()
            self.pie_widget.set_draggable(False)

            self.pie_settings.hide()
            self.accept_button.hide()
            self.settings_button.show()
            self.current_value_holder.hide()

            # Save values from the pie to config
            values = self.pie_widget.order_handler.values
            if self._config.TAG_MODE.read():
                self._group_order_holder.set_order(
                    group_name=self._config.TAG_NAME.read(),
                    values=values)
            else:
                self._config.ORDER.write(values)

            self._is_in_edit_mode = False
        accept_button.clicked.connect(set_edit_mode_off)
        accept_button.hide()

        def move_to_pie_center():
            radius = self._style_holder.pie_style.widget_radius
            accept_button.move_center(QPoint(radius, radius))
        self._register_callback_to_size_change(move_to_pie_center)
        move_to_pie_center()

        return accept_button

    @cached_property
    def current_value_holder(self) -> LabelHolder:
        """Create a LabelWidget holder with currently selected value."""
        style = self._style_holder.small_label_style
        value_holder = LabelHolder(style)
        value_holder.setParent(self.pie_widget)
        value_holder.setAcceptDrops(False)
        value_holder.hide()

        def move_to_bottom_left():
            pie_size = 2*self._style_holder.pie_style.widget_radius
            button_size = 2*self._style_holder.small_label_style.icon_radius
            position = pie_size-button_size
            value_holder.move(QPoint(position, position))
        self._register_callback_to_size_change(move_to_bottom_left)
        move_to_bottom_left()

        def set_enabled():
            current = value_holder.label
            if current is None:
                return
            enabled = current not in self.pie_widget.order_handler.labels
            value_holder.enabled = enabled
        self.pie_widget.order_handler.register_callback_on_change(set_enabled)

        return value_holder

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()

        # This is the first `pie_widget` occurence, which creates it
        if self.pie_widget.isVisible():
            return

        new_labels = self._label_creator.labels_from_config(self._config)
        current_labels = self.pie_widget.order_handler.labels

        if new_labels != current_labels or self._force_reload:
            self._force_reload = False
            self.pie_widget.order_handler.replace_labels(new_labels)

        # Fill current_value_holder with current value
        self._controller.refresh()
        try:
            current_value = self._controller.get_value()
        except NotImplementedError:
            label = None
        else:
            labels = self._label_creator.labels_from_values([current_value])
            label = labels[0] if labels else None
        self.current_value_holder.replace(label)
        self.current_value_holder.enabled = label not in new_labels

        self.pie_actuator.mark_suggested_widget()
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

        if self._is_in_edit_mode:
            return

        # Hide the widget before label gets activated
        # Activation can open windows, which is better with pie hidden
        self.pie_widget.hide()

        label = self.pie_actuator.select()
        if label is not None:
            self._controller.set_value(label.value)
            self._config.LAST_VALUE_SELECTED.write(label.value)

        self.pie_mouse_tracker.stop()

    def _register_callback_to_size_change(self, callback: Callable[[], None]):
        self._config.PIE_RADIUS_SCALE.register_callback(callback)
        self._config.ICON_RADIUS_SCALE.register_callback(callback)
        Config.PIE_GLOBAL_SCALE.register_callback(callback)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(callback)
