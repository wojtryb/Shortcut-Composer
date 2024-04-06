# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from functools import cached_property

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.pyqt import RoundButton
from core_components import Controller, Instruction
from data_components import RotationDeadzoneStrategy
from .raw_instructions import RawInstructions
from .rotation_menu_utils import (
    RotationSettings,
    RotationActuator,
    RotationManager,
    RotationConfig,
    RotationWidget,
    RotationStyle)


class RotationSelector(RawInstructions):
    """
    Pick an angle by hovering over a widget.

    - Widget is displayed under the cursor between key press and release
    - Moving the mouse past deadzone contiguously sets a value
    - Depending on the zone, value is precise or intervallic
    - When in deadzone, selected strategy is used to determine action
    - Edit button activates the setting widget

    ### Arguments:

    - `name`          -- unique name of action. Must match the
                         definition in shortcut_composer.action file
    - `controller`    -- defines which krita property will be modified
    - `instructions`  -- (optional) list of additional instructions to
                         perform on key press and release
    - `is_widget_hidden`    -- (optional) allows to hide the widget
    - `deadzone_scale`      -- (optional) default deadzone size multiplier
    - `inner_zone_scale`    -- (optional) default inner zone size multiplier
    - `is_counterclockwise` -- (optional) default rotation direction
    - `offset`              -- (optional) default offset of zero value
    - `inverse_zones`       -- (optional) default order of zones
    - `divisions` -- (optional) default amount of values in intervallic zone
    - `active_color`      -- (optional) default rgba color of active pie
    - `deadzone strategy` -- (optional) default strategy what to do,
                              when mouse does not leave deadzone
    - `outline_opacity`   -- (optional) default opacity in %
    - `short_vs_long_press_time` -- (optional) time [s] that specifies
                                    if key press is short or long.

    ### Action implementation example:

    Example action is meant to open a widget for rotating a brush.

    ```python
    templates.RotationSelector(
        name="Rotate brush",
        controller=controllers.BrushRotationController(),
        is_counterclockwise=True,  # Rotation is done counter-clockwise
        offset=90,                 # Zero degree is on the right
        inverse_zones=False,       # Intervallic zone is before the precise one
        divisions=24,              # Steps every 15 degrees (360/24)
        deadzone_strategy=RotationDeadzoneStrategy.KEEP_CHANGE,
            # Going back to deadzone will keep the changed value
    )
    ```
    """

    def __init__(
        self, *,
        name: str,
        controller: Controller[int],
        instructions: list[Instruction] | None = None,
        is_widget_hidden: bool = False,
        deadzone_scale: float = 1.0,
        inner_zone_scale: float = 1.0,
        is_counterclockwise: bool = False,
        offset: int = 0,
        inverse_zones: bool = False,
        divisions: int = 24,
        active_color: QColor | None = None,
        deadzone_strategy=RotationDeadzoneStrategy.KEEP_CHANGE,
        outline_opacity: int = 75,
        short_vs_long_press_time: float | None = None,
    ) -> None:
        super().__init__(name, instructions, short_vs_long_press_time)
        self._controller = controller

        self._config = RotationConfig(
            name=self.name,
            is_widget_hidden=is_widget_hidden,
            deadzone_strategy=deadzone_strategy,
            inverse_zones=inverse_zones,
            divisions=divisions,
            deadzone_scale=deadzone_scale,
            inner_zone_scale=inner_zone_scale,
            active_color=active_color,
            outline_opacity=outline_opacity,
            is_counterclockwise=is_counterclockwise,
            offset=offset)

        self._style = RotationStyle(
            deadzone_scale_callback=self._config.DEADZONE_SCALE.read,
            inner_zone_scale_callback=self._config.INNER_ZONE_SCALE.read,
            divisions_callback=self._config.DIVISIONS.read,
            active_color_callback=self._config.ACTIVE_COLOR.read,
            outline_opacity_callback=self._config.OUTLINE_OPACITY.read)

        self._rotation_widget = RotationWidget(
            config=self._config,
            style=self._style)

        self._rotation_manager = RotationManager(
            rotation_widget=self._rotation_widget,
            config=self._config,
            style=self._style)

        self._rotation_actuator = RotationActuator(
            rotation_widget=self._rotation_widget,
            controller=controller,
            config=self._config,
            strategy_field=self._config.DEADZONE_STRATEGY)

    def _create_settings_button(self, parent: QWidget) -> RoundButton:
        """Create button with which user can enter the edit mode."""

        settings_button = RoundButton(
            radius_callback=lambda: self._style.settings_button_radius,
            background_color_callback=Krita.get_main_color_from_theme,
            active_color_callback=Krita.get_active_color_from_theme,
            icon=Krita.get_icon("properties"),
            icon_scale=1.1,
            parent=parent)

        def on_click() -> None:
            self._rotation_widget.hide()
            self._rotation_settings.show()
            self._global_settings_button.hide()
        settings_button.clicked.connect(on_click)

        return settings_button

    @cached_property
    def _settings_button(self) -> RoundButton:
        return self._create_settings_button(self._rotation_widget)

    @cached_property
    def _global_settings_button(self) -> RoundButton:
        return self._create_settings_button(None)  # type: ignore

    @cached_property
    def _rotation_settings(self) -> RotationSettings:
        """Create a settings widget which configures the menu."""
        return RotationSettings(config=self._config)

    def on_key_press(self) -> None:
        """Handle the event of user pressing the action key."""
        super().on_key_press()
        self._controller.refresh()
        self._rotation_manager.start()
        self._rotation_actuator.start()

        self._settings_button.move(QPoint(
            self._rotation_widget.width()-self._settings_button.width(),
            self._rotation_widget.height()-self._settings_button.height()))

        if (self._config.IS_WIDGET_HIDDEN.read()
                and not self._rotation_settings.isVisible()):
            self._global_settings_button.show()
            mdiArea = Krita.get_active_mdi_area()
            self._global_settings_button.move(
                mdiArea.mapToGlobal(mdiArea.pos()))

    def on_every_key_release(self) -> None:
        """Handle the key release event."""
        super().on_every_key_release()
        self._rotation_actuator.stop()
        self._rotation_manager.stop()

        self._global_settings_button.hide()
