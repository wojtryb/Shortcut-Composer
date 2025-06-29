# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from api_krita.enums.helpers import EnumGroup
from core_components import Controller
from composer_utils import ButtonsLayout
from composer_utils.label.complex_widgets import NumericValuePicker

from composer_utils.label import LabelWidgetStyle
from composer_utils.label.complex_widgets import LabelHolder
from ..pie_menu_utils.pie_label_creator_utils import dispatch_pie_group_manager
from ..pie_menu_utils import PieWidget, PieLabelCreator, PieLabel
from ..pie_menu_utils.pie_widget_utils import PieWidgetStyle
from ..pie_menu_utils.pie_settings_tabs import TabValuesList
from .ma_config import MaConfig


class MaSettingsWindow(QDialog):
    """Tab in which user can change action enums and their order."""

    def __init__(self, controller: Controller, config: MaConfig):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(self.minimumSizeHint())

        self._config = config
        self._controller = controller
        self._label_creator = PieLabelCreator(controller)
        self._group_manager = dispatch_pie_group_manager(controller)

        active_color = QColor(110, 160, 255)
        background_color = QColor(150, 150, 255)
        self._pie_style = PieWidgetStyle(
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color,
            background_opacity_callback=lambda: 35)
        self._label_style = LabelWidgetStyle(
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color)

        self._widget = self._init_widget()
        self._holder_of_default = self._init_holder_of_default()
        self._buttons = self._init_buttons()

        self.setLayout(self._init_layout())

    def _init_layout(self) -> QVBoxLayout:
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
        widget = PieWidget(
            pie_style=self._pie_style,
            allowed_types=self._controller.TYPE)

        def set_draggable():
            widget.set_draggable(not self._config.GROUP_MODE.read())
        self._config.GROUP_MODE.register_callback(set_draggable)
        set_draggable()

        return widget

    def _init_holder_of_default(self) -> LabelHolder:
        holder_of_default = LabelHolder(self._label_style)
        holder_of_default.enabled = True
        holder_of_default.setAcceptDrops(True)
        return holder_of_default

    def _init_buttons(self) -> ButtonsLayout:
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

    def _reset_values(self) -> None:
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
        super().show()
        self._reset_values()
        self._widget.setFocus()
