# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor

from api_krita import Krita
from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from composer_utils import ButtonsLayout
from composer_utils.label.complex_widgets import NumericValuePicker

from composer_utils import Config
from composer_utils.group_manager_impl import dispatch_group_manager
from composer_utils.label import LabelWidgetStyle
from composer_utils.label.complex_widgets import LabelHolder
# FIXME PieMenu elements should probably be moved to some common_utils
from ..pie_menu_utils import PieWidget, PieLabelCreator, PieLabel
from ..pie_menu_utils.pie_widget_utils import PieWidgetStyle
from ..pie_menu_utils.pie_settings_tabs import TabValuesList
from .ma_config import MaConfig


class MaSettings(QDialog):
    """
    Widget that allows to change values in a MultipleAssignment action.

    Uses elements from PieMenu action for picking the values to cycle
    using the PieWidget and TabValuesList.

    The widget exists in two modes:
    - In manual mode labels are displayed in scroll area, from which
      they can be dragged into the PieWidget.
    - In group mode, selecting a group automatically puts all of the
      labels that belong to this group to the PieWidget.

    Dragging a label into the LabelHolder on the bottom allows to change
    the value to activate on long key release of action.
    """

    def __init__(self, controller: Controller, config: MaConfig):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint)

        self._config = config
        self._controller = controller
        self._label_creator = PieLabelCreator(controller)
        self._group_manager = dispatch_group_manager(controller.TYPE)

        def pie_widget_radius() -> int:
            """Return radius of the PieWidget."""
            return round(
                0.065 * Krita.screen_size
                * Config.PIE_GLOBAL_SCALE.read())

        def desired_pie_label_radius() -> int:
            """Return max radius of LabelWidget in the PieWidget"""
            return round(
                0.020 * Krita.screen_size
                * Config.PIE_ICON_GLOBAL_SCALE.read())

        active_color = QColor(110, 160, 255)
        background_color = QColor(150, 150, 255)
        self._pie_style = PieWidgetStyle(
            pie_radius_callback=pie_widget_radius,
            desired_icon_radius_callback=desired_pie_label_radius,
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color,
            background_opacity_callback=lambda: 35)
        self._label_style = LabelWidgetStyle(
            icon_radius_callback=desired_pie_label_radius,
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color)
        self._small_label_style = LabelWidgetStyle(
            icon_radius_callback=lambda: round(Krita.screen_size*0.012),
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color)

        self._widget = self._init_widget()
        self._current_value_holder = self._init_current_value_holder()
        self._holder_of_default = self._init_holder_of_default()
        self._buttons = self._init_buttons()

        self.setLayout(self._init_layout())

    def _init_layout(self) -> QVBoxLayout:
        """
        Create MaSettings layout.

        - PieWidget with values to cycle on the left
        - LabelHolder with long-key-press value underneath
        - TabValuesList with values and mode button on the right
        - Reset, Cancel, Apply, OK button in the footer
        """
        bottom_of_left_layout = QHBoxLayout()
        bottom_of_left_layout.addStretch()
        text = QLabel("Value to set\nafter long key press:")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom_of_left_layout.addWidget(text)
        bottom_of_left_layout.addWidget(self._holder_of_default)
        bottom_of_left_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self._widget)
        left_layout.addLayout(bottom_of_left_layout)

        core_layout = QHBoxLayout()
        core_layout.addLayout(left_layout)
        if issubclass(self._controller.TYPE, (str, EnumGroup)):
            tab = TabValuesList(
                config=TabValuesList.Config(
                    self._config.GROUP_MODE,
                    self._config.GROUP_NAME,
                    self._config.LAST_GROUP_SELECTED),
                order_handler=self._widget.order_handler,
                controller=self._controller,
                label_style=self._label_style)
            core_layout.addWidget(tab)
        elif issubclass(self._controller.TYPE, int):
            def label_from_integer(value: int) -> PieLabel[int]:
                label = PieLabel.from_value(value, self._controller)
                if label is None:
                    raise RuntimeError(f"Could not create label from {value}")
                return label
            core_layout.addWidget(NumericValuePicker(label_from_integer))

        layout = QVBoxLayout()
        layout.addLayout(core_layout)
        layout.addLayout(self._buttons)

        return layout

    def _init_widget(self):
        """Create PieWidget with values to cycle."""
        widget = PieWidget(
            style=self._pie_style,
            allowed_types=self._controller.TYPE)
        widget.only_order_change = False

        def set_draggable_in_manual_mode():
            widget.draggable = not self._config.GROUP_MODE.read()
        self._config.GROUP_MODE.register_callback(set_draggable_in_manual_mode)
        set_draggable_in_manual_mode()

        def reset_size() -> None:
            self.hide()
            widget.reset_size()

        Config.PIE_GLOBAL_SCALE.register_callback(reset_size)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(reset_size)

        return widget

    def _init_holder_of_default(self) -> LabelHolder:
        """Create LabelHolder with a value to pick in long-key-press."""
        holder_of_default = LabelHolder(self._label_style)
        holder_of_default.enabled = True
        holder_of_default.setAcceptDrops(True)
        return holder_of_default

    def _init_buttons(self) -> ButtonsLayout:
        """Create ButtonsLayout with Reset, Cancel, Apply and OK."""
        def reset() -> None:
            self._config.reset_default()
            self._reset_values()

        def apply() -> None:
            self._config.VALUES.write(self._widget.order_handler.values)
            label = self._holder_of_default.label
            if label is not None:
                self._config.DEFAULT_VALUE.write(label.value)

        def ok() -> None:
            apply()
            self.hide()

        return ButtonsLayout(
            reset_callback=reset,
            cancel_callback=self.hide,
            apply_callback=apply,
            ok_callback=ok)

    def _init_current_value_holder(self) -> LabelHolder:
        """Widget containing current value."""
        value_holder = LabelHolder(self._small_label_style)
        value_holder.setParent(self._widget)
        value_holder.setAcceptDrops(False)

        # Correct position of the holder is at bottom left
        pie_size = 2*self._pie_style.widget_radius
        button_size = 2*self._small_label_style.icon_radius
        position = pie_size-button_size
        value_holder.move(QPoint(position, position))

        # Holder must be disabled, when its value is already in pie_widget
        def set_enabled():
            current = value_holder.label
            if current is None:
                return
            enabled = current not in self._widget.order_handler.labels
            value_holder.enabled = enabled
        self._widget.order_handler.register_callback_on_change(set_enabled)

        return value_holder

    def _reset_values(self) -> None:
        """Reset values in PieWidget and LabelHolder to defaults."""
        # Reset widget
        if not self._config.GROUP_MODE.read():
            values = self._config.VALUES.read()
        else:
            group = self._config.GROUP_NAME.read()
            values = self._group_manager.values_from_group(group)
        labels = self._label_creator.labels_from_values(values)
        self._widget.order_handler.replace_labels(labels)

        # Reset default value holder
        value = self._config.DEFAULT_VALUE.read()
        label = self._label_creator.label_from_value(value)
        self._holder_of_default.replace(label)

    def show(self) -> None:
        """Show the widget. Fixes the issue of search bar taking focus."""
        super().show()

        self._controller.refresh()
        try:
            current_value = self._controller.get_value()
        except NotImplementedError:
            label = None
        else:
            label = self._label_creator.label_from_value(current_value)
        self._current_value_holder.replace(label)
        enabled = label not in self._widget.order_handler.labels
        self._current_value_holder.enabled = enabled

        self._reset_values()
        self._widget.setFocus()
