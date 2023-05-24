# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from typing import List, Protocol, Callable

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QScroller,
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


class EmptySignal(Protocol):
    """Protocol fixing the wrong PyQt typing."""

    def emit(self) -> None: ...
    def connect(self, method: Callable[[], None]) -> None: ...


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

    widgets_changed: EmptySignal = pyqtSignal()  # type: ignore

    def __init__(
        self,
        style: PieStyle,
        columns: int,
        parent=None
    ) -> None:
        super().__init__(parent)
        self._style = style
        self._columns = columns

        self._known_children: dict[Label, LabelWidget] = {}
        self._children_list: List[LabelWidget] = []

        self._grid = OffsetGridLayout(self._columns, self)
        self._active_label_display = self._init_active_label_display()
        self._search_bar = self._init_search_bar()
        self._layout = self._init_layout()

        self.setLayout(self._layout)

    def _init_layout(self) -> QVBoxLayout:
        """
        Create scroll area layout.

        - most part is taken by the scrollable widget with icons
        - below there is a footer which consists of:
            - label displaying hovered icon name
            - search bar which filters icons
        """
        footer = QHBoxLayout()
        footer.addWidget(self._active_label_display, 1)
        footer.addWidget(self._search_bar, 1)

        layout = QVBoxLayout()
        layout.addWidget(self._init_scroll_area())
        layout.addLayout(footer)
        return layout

    def _init_active_label_display(self):
        class RestrictedLabel(QLabel):
            def setText(self, text: str) -> None:
                if len(text) >= 30:
                    text = f"{text[:27]}..."
                return super().setText(text)
        return RestrictedLabel(self)

    def _init_scroll_area(self) -> QScrollArea:
        """Create a widget, which scrolls internal widget with grid layout."""
        internal = QWidget()
        internal.setLayout(self._grid)

        area = QScrollArea()
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        radius = self._style.unscaled_icon_radius
        area.setMinimumWidth(round(radius*self._columns*2.3))
        area.setMinimumHeight(round(radius*9.2))
        area.setWidgetResizable(True)
        area.setWidget(internal)
        QScroller.grabGesture(
            area.viewport(), QScroller.MiddleMouseButtonGesture)

        return area

    def _init_search_bar(self) -> QLineEdit:
        """Create search bar which hides icons not matching its text."""
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Search")
        search_bar.setClearButtonEnabled(True)
        search_bar.textChanged.connect(self._apply_search_bar_filter)
        return search_bar

    def _apply_search_bar_filter(self) -> None:
        """Replace widgets in layout with those thich match the filter."""
        self.setUpdatesEnabled(False)
        pattern = re.escape(self._search_bar.text())
        regex = re.compile(pattern, flags=re.IGNORECASE)

        children = [child for child in self._children_list
                    if regex.search(child.label.pretty_name)]

        self._grid.replace(children)
        QTimer.singleShot(10, lambda: self.setUpdatesEnabled(True))

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
        self.setUpdatesEnabled(False)
        self._children_list.clear()

        for label in labels:
            if label in self._known_children:
                self._children_list.append(self._known_children[label])
            else:
                self._children_list.append(self._create_child(label))

        self._grid.extend(self._children_list)
        QTimer.singleShot(10, lambda: self.setUpdatesEnabled(True))
        self.widgets_changed.emit()

    def mark_used_values(self, used_values: list) -> None:
        """Make all values currently used in pie undraggable and disabled."""
        for widget in self._children_list:
            if widget.label.value in used_values:
                widget.enabled = False
                widget.draggable = False
            else:
                widget.enabled = True
                widget.draggable = True
