# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from config_system.ui import (
    ConfigFormWidget,
    EnumComboBox,
    ColorButton,
    Checkbox,
    SpinBox)
from data_components import PieDeadzoneStrategy
from ..pie_config import PieConfig


class TabPreferences(QWidget):
    """
    Tab that allows to change preferences of the PieMenu action.

    `requires_text_settings` flag allows to skip segment of form for
    pies which labels never include any text.
    """

    def __init__(
        self,
        config: PieConfig,
        requires_text_settings: bool,
    ) -> None:
        super().__init__(None)
        self._config = config
        self._form = self._init_form(requires_text_settings)
        self._reset_button = self._init_reset_button()
        self.setLayout(self._init_layout())

    def refresh(self) -> None:
        """Change all values in the form to values stored in config."""
        self._form.refresh()

    def apply(self) -> None:
        """Save all values from the form to the config."""
        self._form.apply()

    def _init_layout(self) -> QVBoxLayout:
        """Create layout with form and a button to reset values to default."""
        layout = QVBoxLayout()
        layout.addWidget(self._form)
        layout.addStretch()
        layout.addWidget(self._init_reset_button())
        return layout

    def _init_form(self, requires_text_settings: bool) -> ConfigFormWidget:
        """Create a form widgets that handle some of the config fields."""
        form = ConfigFormWidget([])

        form.add_title("Behavior")
        form.add_row(EnumComboBox(
            config_field=self._config.DEADZONE_STRATEGY,
            parent=self,
            pretty_name="On deadzone",
            enum_type=PieDeadzoneStrategy,
            tooltip=""
            "What to do when the cursor is in deadzone.\n\n"
            "Do nothing: No action is needed.\n"
            "Pick top: Icon on the top is activated.\n"
            "Pick previous: Previously selected icon is activated.\n"
            "    This allows to go back to once selected icon,\n"
            "    when its value is changed by another pie or from\n"
            "    outside of this plugin."))

        form.add_title("Size")
        form.add_row(SpinBox(
            config_field=self._config.PIE_RADIUS_SCALE,
            parent=self,
            pretty_name="Pie scale",
            step=0.05,
            min_value=0.25,
            max_value=4,
            tooltip="Scale of the radius of the entire pie."))
        form.add_row(SpinBox(
            config_field=self._config.ICON_RADIUS_SCALE,
            parent=self,
            pretty_name="Icon max scale",
            step=0.05,
            min_value=0.25,
            max_value=4,
            tooltip=""
            "Scale of the icons maximal radius.\n\n"
            "They can get smaller when there is no space."))

        form.add_title("Style")
        form.add_row(theme_checkbox := Checkbox(
            config_field=self._config.OVERRIDE_DEFAULT_THEME,
            parent=self,
            pretty_name="Override default theme",
            tooltip="Should the colors be set manually."))
        form.add_row(bg_button := ColorButton(
            config_field=self._config.BACKGROUND_COLOR,
            parent=self,
            pretty_name="Background color",
            tooltip="Color of the pie background."))
        form.add_row(active_button := ColorButton(
            config_field=self._config.ACTIVE_COLOR,
            parent=self,
            pretty_name="Active color",
            tooltip="Color of the selected icon indicator."))
        form.add_row(opacity_picker := SpinBox(
            config_field=self._config.PIE_OPACITY,
            parent=self,
            pretty_name="Pie opacity",
            step=1,
            min_value=0,
            max_value=100,
            tooltip="Opacity of the pie background."))

        if requires_text_settings:
            form.add_title("Label text")
            form.add_row(SpinBox(
                config_field=self._config.MAX_LINES_AMOUNT,
                parent=self,
                pretty_name="Max lines amount",
                step=1,
                min_value=1,
                max_value=3,
                tooltip="Maximum number of lines in text label."))
            form.add_row(SpinBox(
                config_field=self._config.MAX_SIGNS_AMOUNT,
                parent=self,
                pretty_name="Max signs amount",
                step=1,
                min_value=3,
                max_value=10,
                tooltip="Maximum number of signs in one line of text label."))
            form.add_row(Checkbox(
                config_field=self._config.ABBREVIATE_WITH_DOT,
                parent=self,
                pretty_name="Abbreviate with dot",
                tooltip="Use '.' sign at the end of abbreviated words."))

        def update_theme_state() -> None:
            """Hide color buttons when not taken into consideration."""
            enable_state = theme_checkbox.widget.isChecked()
            bg_button.widget.setVisible(enable_state)
            active_button.widget.setVisible(enable_state)
            opacity_picker.widget.setEnabled(enable_state)
        theme_checkbox.widget.stateChanged.connect(update_theme_state)
        update_theme_state()

        return form

    def _init_reset_button(self) -> SafeConfirmButton:
        """Create button which resets fields in form to default."""

        def _reset_config_to_default() -> None:
            """
            Reset widgets from preferences layout to default values.

            Does not write to config yet, to prevent artifacts on pie.
            """
            for widget in self._form.widgets:
                widget.set(widget.config_field.default)

        button = SafeConfirmButton(
            text="Reset pie preferences",
            icon=Krita.get_icon("edit-delete"))
        button.clicked.connect(_reset_config_to_default)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button
