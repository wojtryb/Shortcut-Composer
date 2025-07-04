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
from data_components import PieDeadzoneStrategy, Group
from .pie_menu_utils import PieConfig
from .pie_menu_utils import (
    PieLabelSelector,
    PieLabelCreator,
    PieStyleHolder,
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
      release and can be configured (see pie_menu_utils.pie_settings.py)

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.actions.py file
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

    ### Action usage example:

    Example action is meant to change opacity of current layer to one of
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

    PieMenu class represents the entire action for picking values from a
    radial menu. Do not confuse it with PieWidget, which represents the
    GUI of displayed widget.

    PieMenu responsibilities are:
    - creating top-level action components (for both GUI and logic).
    - connecting those components together.
    - handling the KeyPress and KeyRelease events of the
      ComplexActionInterface it implements.

    PieMenu action exists in two main states:
    - When in normal mode:
        - Action closes on KeyRelease event.
        - Action is used for activating displayed values.
        - `pie_widget` is shown, `settings` is hidden.
        - Values displayed on `pie_widget` cannot be dragged.
        - `settings_button` is shown. It allows to enter the edit mode.

    - Wnen in edit mode:
        - Action can be closed only with the `accept_button`.
        - Action is used for selecting what values will be displayed
          after returning to normal mode.
        - Both `pie_widget` and `settings` are shown.
        - labels can be dragged to, from and into the `pie_widget`.
        - `settings_button` is replaced with `current_value_holder`

    Created components are defined as `cached_property`. As GUI can take
    a relatively long time to initialize, this solution allows to create
    them at the moment user activates them:
    - `pie_widget` is created on first KeyPress of this action.
    - `settings` is created on first entering of the edit mode.

    All components that require those components during initialization
    also need to be defined as `cached_property`.
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[T],
        values: list[T] | Group,
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
        self._label_creator = PieLabelCreator(self._controller)
        self._group_order_holder = GroupOrderHolder(self._controller.TYPE)

        self._is_in_edit_mode = False
        self._force_reload = False

        # Usually, when values stay same, recreating widgets is not
        # needed, but when widget scale changes, they have to be
        # reloaded even when values were not changed.
        def raise_flag():
            self._force_reload = True
        self._register_callback_to_size_change(raise_flag)
        self._config.MAX_SIGNS_AMOUNT.register_callback(raise_flag)
        self._config.MAX_LINES_AMOUNT.register_callback(raise_flag)
        self._config.ABBREVIATE_WITH_DOT.register_callback(raise_flag)

    @cached_property
    def _pie_widget(self) -> PieWidget:
        """GUI of the radial menu for activating values."""

        pie_widget = PieWidget(
            style=self._style_holder.pie_widget_style,
            allowed_types=self._controller.TYPE)
        pie_widget.draggable = False

        def allow_value_edit():
            pie_widget.only_order_change = self._config.GROUP_MODE.read()
        self._config.GROUP_MODE.register_callback(allow_value_edit)
        allow_value_edit()

        def reset_size():
            pie_widget.hide()
            pie_widget.reset_size()
        self._register_callback_to_size_change(reset_size)

        self._settings_button.setParent(pie_widget)

        return pie_widget

    @cached_property
    def _settings(self) -> PieSettings:
        """GUI for customizing the pie_widget in the edit mode."""
        settings = PieSettings(
            config=self._config,
            style_holder=self._style_holder,
            controller=self._controller,
            order_handler=self._pie_widget.order_handler)

        self._register_callback_to_size_change(settings.hide)
        return settings

    @cached_property
    def _label_selector(self) -> PieLabelSelector:
        """Logic of showing/hiding/moving pie_widget in normal mode."""
        last_value = self._config.LAST_VALUE_SELECTED.read()
        label = self._label_creator.label_from_value(last_value)

        label_selector = PieLabelSelector(
            pie_widget=self._pie_widget,
            initial_label=label)

        def update_strategy() -> None:
            label_selector.strategy = self._config.DEADZONE_STRATEGY.read()
        self._config.DEADZONE_STRATEGY.register_callback(update_strategy)
        update_strategy()

        return label_selector

    @cached_property
    def _settings_button(self) -> RoundButton:
        """GUI for switching from normal to edit mode."""
        pie_style = self._style_holder.pie_widget_style

        settings_button = RoundButton(
            radius_callback=lambda: self._style_holder.settings_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("properties"),
            icon_scale=1.1)

        def set_edit_mode_on() -> None:
            # Following cached_property are created in this method:
            # self._settings
            # self._accept_button
            # self._current_value_holder

            self._label_selector.stop_tracking()

            self._pie_widget.draggable = True
            self._pie_widget.repaint()

            # Move settings next to the pie
            self._settings.show()
            pie_radius = self._style_holder.pie_widget_style.widget_radius
            offset = round(pie_radius + self._settings.width()*0.525)
            center = self._pie_widget.center_global + QPoint(offset, 0)
            self._settings.move_center(center)

            self._accept_button.show()
            self._settings_button.hide()
            self._current_value_holder.show()

            self._is_in_edit_mode = True
        settings_button.clicked.connect(set_edit_mode_on)  # type:ignore

        def move_to_bottom_left():
            pie_size = 2*self._style_holder.pie_widget_style.widget_radius
            button_size = 2*self._style_holder.small_label_style.icon_radius
            position = pie_size-button_size
            settings_button.move(QPoint(position, position))
        self._register_callback_to_size_change(move_to_bottom_left)
        move_to_bottom_left()

        return settings_button

    @cached_property
    def _accept_button(self) -> RoundButton:
        """GUI for switching from edit to normal mode."""
        pie_style = self._style_holder.pie_widget_style

        accept_button = RoundButton(
            radius_callback=lambda: self._style_holder.accept_button_radius,
            background_color_callback=lambda: pie_style.background_color,
            active_color_callback=lambda: pie_style.active_color,
            icon=Krita.get_icon("dialog-ok"),
            icon_scale=1.5,
            parent=self._pie_widget)

        def set_edit_mode_off():
            self._pie_widget.hide()
            self._settings.hide()
            self._accept_button.hide()
            self._settings_button.show()
            self._current_value_holder.hide()

            # Save values from the pie to config
            values = self._pie_widget.order_handler.values
            if self._config.GROUP_MODE.read():
                self._group_order_holder.set_order(
                    group_name=self._config.GROUP_NAME.read(),
                    values=values)
            else:
                self._config.ORDER.write(values)

            self._is_in_edit_mode = False
        accept_button.clicked.connect(set_edit_mode_off)  # type:ignore
        accept_button.hide()

        # Correct position of the button is at the center of pie_widget
        def move_to_pie_center():
            radius = self._style_holder.pie_widget_style.widget_radius
            accept_button.move_center(QPoint(radius, radius))
        self._register_callback_to_size_change(move_to_pie_center)
        move_to_pie_center()

        return accept_button

    @cached_property
    def _current_value_holder(self) -> LabelHolder:
        """GUI containing current value in edit mode."""
        style = self._style_holder.small_label_style
        value_holder = LabelHolder(style)
        value_holder.setParent(self._pie_widget)
        value_holder.setAcceptDrops(False)
        value_holder.hide()

        # Correct position of the holder is at bottom left
        def move_to_bottom_left():
            value_holder.reset_size()
            pie_size = 2*self._style_holder.pie_widget_style.widget_radius
            button_size = 2*self._style_holder.small_label_style.icon_radius
            position = pie_size-button_size
            value_holder.move(QPoint(position, position))
        self._register_callback_to_size_change(move_to_bottom_left)
        move_to_bottom_left()

        # Holder must be disabled, when its value is already in pie_widget
        def set_enabled():
            current = value_holder.label
            if current is None:
                return
            enabled = current not in self._pie_widget.order_handler.labels
            value_holder.enabled = enabled
        self._pie_widget.order_handler.register_callback_on_change(set_enabled)

        return value_holder

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()

        # Following cached_property are created in this method:
        # self._pie_widget
        # self._settings_button (technically created by pie_widget)
        # self._label_selector

        # Abort handling when the widget is already being displayed
        if self._pie_widget.isVisible():
            return

        # Read values selected for display from config
        new_labels = self._label_creator.labels_from_config(self._config)
        current_labels = self._pie_widget.order_handler.labels

        # Replace labels in pie_widget when values or label size changed
        if new_labels != current_labels or self._force_reload:
            self._force_reload = False
            self._pie_widget.order_handler.replace_labels(new_labels)

        # Fill current_value_holder with value from controller
        self._controller.refresh()
        try:
            current_value = self._controller.get_value()
        except NotImplementedError:
            label = None
        else:
            label = self._label_creator.label_from_value(current_value)
        self._current_value_holder.replace(label)
        self._current_value_holder.enabled = label not in new_labels

        # Start tracker which highlights/selects the values under cursor
        self._label_selector.start_tracking()

    def on_every_key_release(self) -> None:
        """Handle the event of user releasing the action key."""
        super().on_every_key_release()

        if self._is_in_edit_mode:
            return

        label = self._label_selector.select()
        self._label_selector.stop_tracking()

        # Hide the pie_widget before label gets activated. Activation
        # could open windows, which is better with it being hidden
        self._pie_widget.hide()

        # If actuator selected a value, activate, and remember it.
        # Remembered value will initialize actuator in next session
        if label is not None:
            self._controller.set_value(label.value)
            self._config.LAST_VALUE_SELECTED.write(label.value)

    def _register_callback_to_size_change(self, callback: Callable[[], None]):
        """Register callback to each config Field related to size."""
        self._config.PIE_RADIUS_SCALE.register_callback(callback)
        self._config.ICON_RADIUS_SCALE.register_callback(callback)
        Config.PIE_GLOBAL_SCALE.register_callback(callback)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(callback)
