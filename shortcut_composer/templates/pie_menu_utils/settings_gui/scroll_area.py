# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from typing import List

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout)

from ..label import Label
from ..label_widget import LabelWidget
from ..label_widget_utils import create_label_widget
from ..pie_style import PieStyle
from .offset_grid_layout import OffsetGridLayout


class ChildInstruction:
    """Logic of displaying widget text in passed QLabel."""

    def __init__(self, display_label: QLabel) -> None:
        self._display_label = display_label

    def on_enter(self, label: Label) -> None:
        """Set text of label which was entered with mouse."""
        self._display_label.setText(str(label.pretty_name))

    def on_leave(self, label: Label) -> None:
        """Reset text after mouse leaves the widget."""
        self._display_label.setText("")


class ScrollArea(QWidget):
    """
    Widget containing a scrollable list of PieWidgets.

    Widgets are defined with replace_handled_labels method which
    creates the widgets representing them if needed. Using the method
    again will replace handled widgets with new ones representing newer
    passed labels.

    All the created widgets are stored in case they may need to be
    reused when labels change again.

    Currently handled widgets are publically available, so that the
    class owner can change their state (draggable, enabled).

    ScrollArea comes with embedded QLabel showing the name of the
    children widget over which mouse was hovered, and a filter bar.

    Writing something to the filter results in widgets which do not
    match the phrase to not be displayed. Hidden widgets, are still
    available under children_list.
    """

    def __init__(
        self,
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        super().__init__(parent)
        self._style = style

        scroll_widget = QWidget()
        self._scroll_area_layout = OffsetGridLayout(columns, self)
        scroll_widget.setLayout(self._scroll_area_layout)

        area = QScrollArea()
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        area.setMinimumWidth(
            round(self._style.unscaled_icon_radius*columns*2.3))
        area.setMinimumHeight(
            round(self._style.unscaled_icon_radius*9.2))
        area.setWidgetResizable(True)
        area.setWidget(scroll_widget)

        footer = QHBoxLayout()
        self._active_label_display = QLabel(self)
        footer.addWidget(self._active_label_display, 1)
        self._search_bar = QLineEdit(self)
        self._search_bar.setPlaceholderText("Search")
        self._search_bar.setClearButtonEnabled(True)
        footer.addWidget(self._search_bar, 1)
        self._search_bar.textChanged.connect(self._apply_search_bar_filter)

        self._layout = QVBoxLayout()
        self._layout.addWidget(area)
        self._layout.addLayout(footer)
        self.setLayout(self._layout)

        self._known_children: dict[Label, LabelWidget] = {}
        self._children_list: List[LabelWidget] = []

    def _create_child(self, label: Label) -> LabelWidget:
        """Create LabelWidget that represent the label."""
        child = create_label_widget(
            label=label,
            style=self._style,
            parent=self,
            is_unscaled=True)
        child.setFixedSize(child.icon_radius*2, child.icon_radius*2)
        child.draggable = True
        child.add_instruction(ChildInstruction(self._active_label_display))

        self._known_children[label] = child
        return child

    def replace_handled_labels(self, labels: List[Label]) -> None:
        """Replace current list of widgets with new ones."""
        # HACK: disable painting for short time to prevent artifacts
        self.setUpdatesEnabled(False)
        self._children_list.clear()

        for label in labels:
            if label in self._known_children:
                self._children_list.append(self._known_children[label])
            else:
                self._children_list.append(self._create_child(label))

        self._scroll_area_layout.extend(self._children_list)
        QTimer.singleShot(10, lambda: self.setUpdatesEnabled(True))

    def _apply_search_bar_filter(self):
        """Replace widgets in layout with those thich match the filter."""
        self.setUpdatesEnabled(False)
        pattern = re.escape(self._search_bar.text())
        regex = re.compile(pattern, flags=re.IGNORECASE)

        children = [child for child in self._children_list
                    if regex.search(child.label.pretty_name)]

        self._scroll_area_layout.replace(children)
        QTimer.singleShot(10, lambda: self.setUpdatesEnabled(True))

    def mark_used_values(self, used_values: list):
        """Make all values currently used in pie undraggable and disabled."""
        for widget in self._children_list:
            if widget.label.value in used_values:
                widget.enabled = False
                widget.draggable = False
            else:
                widget.enabled = True
                widget.draggable = True
