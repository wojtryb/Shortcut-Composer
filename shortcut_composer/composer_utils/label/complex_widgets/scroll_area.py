# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

import re
from typing import Sequence, TypeVar, Generic

from PyQt5.QtCore import Qt, QTimer, QEvent, pyqtSignal
from PyQt5.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QScroller,
    QLineEdit,
    QWidget,
    QLabel)

from ...global_config import Config
from ..label_widget import LabelWidget, WidgetInstructions
from ..label_widget_style import LabelWidgetStyle
from ..label_widget_impl import dispatch_label_widget
from ..label_interface import LabelInterface
from .scroll_area_utils import OffsetGridLayout

T = TypeVar("T", bound=LabelInterface, contravariant=True)


class ScrollArea(QWidget, Generic[T]):
    """
    Widget containing a scrollable list of PieWidgets.

    Widgets are defined with replace_handled_labels method which
    creates the widgets representing them if needed. Using the method
    again will replace handled widgets with new ones representing newer
    passed labels.

    All the created widgets are stored in case they may need to be
    reused when labels change again.

    Currently handled widgets are publicly available, so that the
    class owner can change their state (draggable, enabled).

    ScrollArea comes with embedded QLabel showing the name of the
    children widget over which mouse was hovered, and a filter bar.

    Writing something to the filter results in widgets which do not
    match the phrase to not be displayed. Hidden widgets, are still
    available under children_list.
    """

    widgets_changed = pyqtSignal()

    def __init__(
        self,
        label_style: LabelWidgetStyle = LabelWidgetStyle(),
        columns: int = 3,
    ) -> None:
        super().__init__(None)
        self._label_style = label_style
        self._columns = columns

        self._known_children: dict[LabelInterface, LabelWidget[T]] = {}
        self._children_list: list[LabelWidget[T]] = []

        self._grid = OffsetGridLayout(self._columns, self)
        self._value_label = self._init_value_label()
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
        footer.addWidget(self._value_label, 1)
        footer.addWidget(self._search_bar, 1)

        layout = QVBoxLayout()
        layout.addWidget(self._init_scroll_area())
        layout.addLayout(footer)
        return layout

    def _init_value_label(self) -> QLabel:
        """Return a label displaying hovered label."""
        label = QLabel(self)
        label.setWordWrap(True)

        def reset_size() -> None:
            # NOTE: Size is fixed due to issue in Qt5 under Windows 10
            label.setFixedWidth(self._label_style.icon_radius*4)
            label.setFixedHeight(label.sizeHint().height()*2)
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(reset_size)
        reset_size()

        return label

    def _init_scroll_area(self) -> QScrollArea:
        """Create a widget, which scrolls internal widget with grid layout."""
        internal = QWidget()
        internal.setLayout(self._grid)

        area = QScrollArea()
        area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        area.setWidgetResizable(True)
        area.setWidget(internal)
        QScroller.grabGesture(
            area.viewport(),
            QScroller.ScrollerGestureType.MiddleMouseButtonGesture)

        def reset_size() -> None:
            # NOTE: Height is fixed due to issue in Qt5 under Windows 10
            radius = self._label_style.icon_radius
            area.setMinimumWidth(round(radius*self._columns*2.3))
            area.setFixedHeight(round(radius*9.2))
        Config.PIE_ICON_GLOBAL_SCALE.register_callback(reset_size)
        reset_size()

        return area

    def _init_search_bar(self) -> QLineEdit:
        """Create search bar which hides icons not matching its text."""
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText("Search")
        search_bar.setClearButtonEnabled(True)
        search_bar.textChanged.connect(self.apply_search_bar_filter)
        return search_bar

    def apply_search_bar_filter(self) -> None:
        """Replace widgets in layout with those that match the filter."""
        self.setUpdatesEnabled(False)
        pattern = re.escape(self._search_bar.text())
        regex = re.compile(pattern, flags=re.IGNORECASE)

        children = [child for child in self._children_list
                    if regex.search(child.label.pretty_name)]

        self._grid.replace(children)
        QTimer.singleShot(10, lambda: self.setUpdatesEnabled(True))

    def _create_child(self, label: LabelInterface) -> LabelWidget[T]:
        """Create LabelWidget[LabelInterface] that represent the label."""
        child = dispatch_label_widget(label)(
            label=label,
            label_widget_style=self._label_style,
            parent=self)
        child.setFixedSize(child.icon_radius*2, child.icon_radius*2)
        child.draggable = True
        child.add_instruction(ChildInstruction(self._value_label))

        self._known_children[label] = child
        return child

    def replace_handled_labels(self, labels: Sequence[LabelInterface]) -> None:
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
        """Make all values currently used in pie non draggable and disabled."""
        for widget in self._children_list:
            if widget.label.value in used_values:
                widget.enabled = False
                widget.draggable = False
            else:
                widget.enabled = True
                widget.draggable = True

    def leaveEvent(self, e: QEvent) -> None:
        """Notice that mouse moved out of the widget."""
        super().leaveEvent(e)
        self._value_label.setText("")


class ChildInstruction(WidgetInstructions):
    """Logic of displaying widget text in passed QLabel."""

    def __init__(self, value_label: QLabel) -> None:
        self._value_label = value_label

    def on_enter(self, label: LabelInterface) -> None:
        """Set text of label which was entered with mouse."""
        self._value_label.setText(label.pretty_name)

    def on_leave(self, label: LabelInterface) -> None:
        pass
