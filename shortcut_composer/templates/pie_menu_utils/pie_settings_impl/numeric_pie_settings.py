# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QSpinBox,
    QWidget,
    QLabel)

from core_components import Controller
from templates.pie_menu_utils.pie_config_impl import NonPresetPieConfig
from templates.pie_menu_utils import Label, PieStyle, PieSettings
from templates.pie_menu_utils.label_widget_impl import dispatch_label_widget


class NumericValuePicker(QWidget):
    def __init__(
        self,
        controller: Controller[float],
        style: PieStyle,
        parent=None
    ):
        super().__init__(parent)

        self._controller = controller
        self._style = style

        self._icon = self._refresh_icon(0)

        def update_icon(a0: int):
            self._icon = self._refresh_icon(a0)
            self._area.setWidget(self._icon)

        self._spin_box = QSpinBox()
        self._spin_box.setMinimum(0)
        self._spin_box.setMaximum(10_000)
        self._spin_box.valueChanged.connect(update_icon)

        self._area = QScrollArea()
        self._area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._area.setWidget(self._icon)
        self._area.setFixedSize(
            round(self._icon.width()*1.1), round(self._icon.height()*1.1))
        self._area.setAlignment(Qt.AlignCenter)
        self._area.setSizeAdjustPolicy(QScrollArea.AdjustIgnored)

        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignTop)
        right_side.addWidget(QLabel("\nSet icon value:"))
        right_side.addWidget(self._spin_box)

        self._layout = QHBoxLayout()
        self._layout.setAlignment(Qt.AlignTop)
        self._layout.addWidget(self._area, 1, Qt.AlignTop)
        self._layout.addLayout(right_side, 1)

        self.setLayout(self._layout)

    def _refresh_icon(self, value: int):
        label = Label.from_value(value, self._controller)

        if label is None:
            raise Exception

        icon = dispatch_label_widget(label)(
            label=label,
            style=self._style,
            parent=self,
            is_unscaled=True)
        icon.setFixedSize(icon.icon_radius*2, icon.icon_radius*2)
        icon.draggable = True

        return icon


class NumericPieSettings(PieSettings):
    """Pie setting window for pie values being numeric (int)."""

    def __init__(
        self,
        controller: Controller[float],
        config: NonPresetPieConfig,
        style: PieStyle,
        *args, **kwargs
    ) -> None:
        super().__init__(config, style)

        self._numeric_picker = NumericValuePicker(controller, style)

        self._tab_holder.insertTab(1, self._numeric_picker, "Values")
        self._tab_holder.setCurrentIndex(1)
