# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable, TypeVar, Generic

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QSpinBox,
    QWidget,
    QLabel)

from composer_utils.label import LabelWidgetStyle, LabelWidget
from composer_utils.label.label_widget_impl import dispatch_label_widget
from ..label_interface import LabelInterface

T = TypeVar("T", bound=LabelInterface[int])


class NumericValuePicker(QWidget, Generic[T]):
    """Widget that displays draggable LabelWidget with value set in SpinBox."""

    def __init__(
        self,
        create_label_from_integer: Callable[[int], T],
        unscaled_label_style: LabelWidgetStyle,
        min_value: int = 0,
        max_value: int = 100,
        step: int = 1,
        wrapping: bool = False,
        adaptive: bool = False,
        parent=None
    ) -> None:
        super().__init__(parent)

        self._create_label_from_integer = create_label_from_integer
        self._unscaled_label_style = unscaled_label_style

        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._wrapping = wrapping
        self._adaptive = adaptive

        self._icon = self._create_icon(value=0)
        self._spin_box = self._init_spin_box()
        self._icon_holder = self._init_icon_holder()
        self._layout = self._init_layout()

        self.setLayout(self._layout)

    def _init_layout(self) -> QHBoxLayout:
        """
        Return layout of the widget.

        - On the left, there is a LabelWidget with set value.
        - On the right, there is a spinbox to set a value in the label.
        """
        right_side = QVBoxLayout()
        right_side.setAlignment(Qt.AlignTop)
        right_side.addWidget(QLabel("\nSet icon value:"))
        right_side.addWidget(self._spin_box)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self._icon_holder, 1, Qt.AlignTop)
        layout.addLayout(right_side, 1)

        return layout

    def _create_icon(self, value: int) -> LabelWidget[T]:
        """Create LabelWidget with given value."""
        label = self._create_label_from_integer(value)

        icon = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._unscaled_label_style,
            parent=self)
        icon.setFixedSize(icon.icon_radius*2, icon.icon_radius*2)
        icon.draggable = True

        return icon

    def _init_spin_box(self) -> QSpinBox:
        """Return spinbox."""
        def update_icon(a0: int) -> None:
            self._icon = self._create_icon(a0)
            self._icon_holder.setWidget(self._icon)

        spin_box = QSpinBox()
        spin_box.setMinimum(self._min_value)
        spin_box.setMaximum(self._max_value)
        spin_box.setSingleStep(self._step)
        spin_box.setWrapping(self._wrapping)
        if self._adaptive:
            spin_box.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        spin_box.valueChanged.connect(update_icon)
        return spin_box

    def _init_icon_holder(self) -> QScrollArea:
        """Return QScrollArea that can hold the LabelWidget."""
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
