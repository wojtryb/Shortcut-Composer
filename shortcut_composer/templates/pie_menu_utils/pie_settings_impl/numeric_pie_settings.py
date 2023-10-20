# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QSpinBox,
    QWidget,
    QLabel)

from core_components import NumericController
from composer_utils import Label
from composer_utils.label_widget_impl import dispatch_label_widget
from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from templates.pie_menu_utils import PieStyle, PieSettings


class NumericValuePicker(QWidget):
    def __init__(
        self,
        controller: NumericController,
        pie_style: PieStyle,
        parent=None
    ) -> None:
        super().__init__(parent)

        self._controller = controller
        self._pie_style = pie_style

        self._icon = self._create_icon(value=0)
        self._spin_box = self._init_spin_box()
        self._icon_holder = self._init_icon_holder()
        self._layout = self._init_layout()

        self.setLayout(self._layout)

    def _init_layout(self):
        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignTop)
        right_side.addWidget(QLabel("\nSet icon value:"))
        right_side.addWidget(self._spin_box)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._icon_holder, 1, Qt.AlignTop)
        layout.addLayout(right_side, 1)

        return layout

    def _create_icon(self, value: int):
        label = Label.from_value(value, self._controller)

        if label is None:
            raise Exception

        icon = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._pie_style.label_style,
            parent=self,
            is_unscaled=True)
        icon.setFixedSize(icon.icon_radius*2, icon.icon_radius*2)
        icon.draggable = True

        return icon

    def _init_spin_box(self):
        def update_icon(a0: int):
            self._icon = self._create_icon(a0)
            self._icon_holder.setWidget(self._icon)

        spin_box = QSpinBox()
        spin_box.setMinimum(self._controller.MIN_VALUE)
        spin_box.setMaximum(self._controller.MAX_VALUE)
        spin_box.setSingleStep(self._controller.STEP)
        spin_box.setWrapping(self._controller.WRAPPING)
        if self._controller.ADAPTIVE:
            spin_box.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        spin_box.valueChanged.connect(update_icon)
        return spin_box

    def _init_icon_holder(self):
        icon_holder = QScrollArea()
        icon_holder.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        icon_holder.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        icon_holder.setWidget(self._icon)
        icon_holder.setAlignment(Qt.AlignCenter)
        icon_holder.setSizeAdjustPolicy(QScrollArea.AdjustIgnored)
        icon_holder.setFixedSize(
            round(self._icon.width()*1.1),
            round(self._icon.height()*1.1))
        return icon_holder


class NumericPieSettings(PieSettings):
    """Pie setting window for pie values being numeric (int)."""

    def __init__(
        self,
        controller: NumericController,
        config: NonPresetPieConfig,
        pie_style: PieStyle,
        *args, **kwargs
    ) -> None:
        super().__init__(config, pie_style)

        self._numeric_picker = NumericValuePicker(controller, pie_style)

        self._tab_holder.insertTab(1, self._numeric_picker, "Values")
        self._tab_holder.setCurrentIndex(1)
