# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from core_components import Controller
from config_system.ui import StringComboBox
from composer_utils import ButtonsLayout
from composer_utils.label.complex_widgets import ScrollArea

from composer_utils.label import LabelWidgetStyle
from ..pie_menu_utils import PieWidget, PieStyle
from ..pie_menu_utils.group_manager_impl import dispatch_group_manager
from .ma_config import MaConfig


# TODO: SettingsWindow
class ActionValuesWindow(QDialog):
    """Tab in which user can change action enums and their order."""

    def __init__(self, controller: Controller, config: MaConfig):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint)

        self._config = config
        self._label_creator = dispatch_group_manager(controller)

        self._scroll_area = ScrollArea(LabelWidgetStyle(
            background_color_callback=lambda: QColor(200, 250, 250),
            active_color_callback=lambda: QColor(225, 255, 255)))
        self._combobox = self._init_combobox()
        self._widget = self._init_widget()
        self._buttons = ButtonsLayout(
            ok_callback=self.hide,
            apply_callback=self.hide,
            reset_callback=self.hide,
            cancel_callback=self.hide)

        self.setLayout(self._init_layout())

    def _init_layout(self) -> QVBoxLayout:
        picker_layout = QVBoxLayout()
        picker_layout.addWidget(self._combobox.widget)
        picker_layout.addWidget(self._scroll_area)

        core_layout = QHBoxLayout()
        core_layout.addWidget(self._widget)
        core_layout.addLayout(picker_layout)

        layout = QVBoxLayout()
        layout.addLayout(core_layout)
        layout.addLayout(self._buttons)

        return layout

    def _init_widget(self):
        widget = PieWidget(PieStyle(
            active_color_callback=lambda: QColor(225, 255, 255),
            background_color_callback=lambda: QColor(150, 150, 255),
            background_opacity_callback=lambda: 35))

        values = self._config.VALUES.read()
        for label in self._label_creator.labels_from_values(values):
            widget.order_handler.append(label)

        widget.set_draggable(True)
        return widget

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

    def show(self):
        super().show()
        self._buttons._button_box.setFocus()
