# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from core_components import Controller
from config_system.ui import StringComboBox
from composer_utils import ButtonsLayout
from composer_utils.label.complex_widgets import ScrollArea

from composer_utils.label import LabelWidgetStyle
from composer_utils.label.complex_widgets import LabelHolder
from ..pie_menu_utils import PieWidget
from ..pie_menu_utils.pie_widget_utils import PieWidgetStyle
from ..pie_menu_utils.pie_label_creator_impl import dispatch_pie_label_creator
from .ma_config import MaConfig


class MaSettingsWindow(QDialog):
    """Tab in which user can change action enums and their order."""

    def __init__(self, controller: Controller, config: MaConfig):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint)

        self._config = config
        self._label_creator = dispatch_pie_label_creator(controller)

        active_color = QColor(110, 160, 255)
        background_color = QColor(150, 150, 255)
        self._pie_style = PieWidgetStyle(
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color,
            background_opacity_callback=lambda: 35)
        self._label_style = LabelWidgetStyle(
            active_color_callback=lambda: active_color,
            background_color_callback=lambda: background_color)

        self._scroll_area = ScrollArea(self._label_style)
        self._combobox = self._init_combobox()
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

        right_layout = QVBoxLayout()
        right_layout.addWidget(self._combobox.widget)
        right_layout.addWidget(self._scroll_area)

        core_layout = QHBoxLayout()
        core_layout.addLayout(left_layout)
        core_layout.addLayout(right_layout)

        layout = QVBoxLayout()
        layout.addLayout(core_layout)
        layout.addLayout(self._buttons)

        return layout

    def _init_widget(self):
        widget = PieWidget(self._pie_style)
        widget.set_draggable(True)
        return widget

    def _init_holder_of_default(self) -> LabelHolder:
        holder_of_default = LabelHolder(self._label_style)
        holder_of_default.enabled = True
        holder_of_default.setAcceptDrops(True)
        return holder_of_default

    def _init_combobox(self) -> StringComboBox:
        def display_group() -> None:
            """Update preset widgets according to tag selected in combobox."""
            picked_group = combobox.read()
            labels = self._label_creator.labels_from_group(
                group=picked_group,
                sort=False)
            self._scroll_area.replace_handled_labels(labels)
            self._scroll_area.apply_search_bar_filter()
            combobox.save()

        combobox = StringComboBox(
            config_field=self._config.LAST_GROUP_SELECTED,
            allowed_values=(
                ["---Select group---", "All"]
                + self._label_creator.fetch_groups()))

        combobox.widget.currentTextChanged.connect(display_group)
        display_group()

        return combobox

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
        values = self._config.VALUES.read()
        labels = self._label_creator.labels_from_values(values)
        self._widget.order_handler.replace_labels(labels)

        # Reset default value holder
        value = self._config.DEFAULT_VALUE.read()
        labels = self._label_creator.labels_from_values((value,))
        label = labels[0] if labels else None
        self._holder_of_default.replace(label)

    def show(self) -> None:
        super().show()
        self._reset_values()
        self._widget.setFocus()
