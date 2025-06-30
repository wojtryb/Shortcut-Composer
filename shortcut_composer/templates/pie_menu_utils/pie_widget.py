# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TypeVar, Generic, Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QPaintEvent)

from api_krita.pyqt import Painter, AnimatedWidget, BaseWidget
from composer_utils import CirclePoints, Config
from composer_utils.label import LabelWidget
from .pie_label import PieLabel
from .pie_widget_utils.pie_widget_style import PieWidgetStyle
from .pie_widget_utils import PieWidgetOrder, PieWidgetPainter

T = TypeVar('T')


class PieWidget(AnimatedWidget, BaseWidget, Generic[T]):
    """
    Custom, circular PyQt widget with LabelWidgets on its edge.

    PieWidget responsibilities are:
    - display values stored in public `order_handler`.
    - handle drag&drop events, allowing to change displayed values.

    The widget is designed to be independent from the PieMenu action.
    It can be connected with other PieMenu components, but on its own
    pie_widget is not aware of the action logic.

    ### Arguments:

    - `pie_style`     -- (optional) specifies visuals of the widget such
                         as size and color of its elements.
    - `allowed_types` -- (optional) types of values that can be dragged
                         into the widget. Other types are ignored.

    ### Public attributes

    - `order_handler` -- use it to populate the widget with values
    - `active_label`  -- unhandled attribute. Other classes can store
                         or use information here. FIXME
    - `draggable`     -- when True, widget allows to drag values from
                         and into itself.
    - `only_order_change` -- when True, widget allows only to swap
                             order of the values with dragging.
                             Adding or removing values is not possible.

    ### Class usage example

    Following example contains three values of int and string types.
    Those three values can be dragged around, but no values can be added
    or removed from the widget.
    The widget is white, and has a random size every time it opens.

    ```python
    import random
    from PyQt5.QtGui import QColor
    from composer_utils.label import LabelText
    from .pie_label import PieLabel
    from .pie_widget import PieWidget
    from .pie_widget_utils import PieWidgetStyle

    pie_widget = PieWidget(
        pie_style=PieWidgetStyle(
            pie_radius_callback=lambda: random.randint(100, 200),
            active_color_callback=lambda: QColor(255, 255, 255)),
        allowed_types=(str, int))

    pie_widget.order_handler.append(PieLabel(1, LabelText("1")))
    pie_widget.order_handler.append(PieLabel(2, LabelText("2")))
    pie_widget.order_handler.append(PieLabel("A", LabelText("A")))

    pie_widget.draggable = True
    pie_widget.only_order_change = True
    ```
    """

    def __init__(
        self,
        pie_style: PieWidgetStyle = PieWidgetStyle(),
        allowed_types: type | tuple[type, ...] = object,
    ) -> None:
        AnimatedWidget.__init__(
            self,
            animation_time_s=Config.PIE_ANIMATION_TIME.read(),
            fps_limit=Config.FPS_LIMIT.read())

        self.setWindowFlags((
            self.windowFlags() |
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.NoDropShadowWindowHint))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setCursor(Qt.CursorShape.CrossCursor)

        self._pie_style = pie_style
        self._allowed_types = allowed_types

        self._painter = PieWidgetPainter(self._pie_style)
        self._last_widget = None

        self.order_handler = PieWidgetOrder(self._pie_style, owner=self)
        self.active_label: PieLabel | None = None
        self.draggable = False
        self.only_order_change = False

        self.reset_size()

    @property
    def draggable(self) -> bool:
        """Does widget allow to drag values from and into itself."""
        return self._draggable

    @draggable.setter
    def draggable(self, draggable: bool) -> None:
        """Set value of `draggable` property."""
        self._draggable = draggable
        for widget in self.order_handler.widgets:
            widget.draggable = self._draggable
        self.setAcceptDrops(self._draggable)

    @property
    def deadzone(self) -> float:
        """Return the deadzone distance."""
        return self._pie_style.deadzone_radius

    def paintEvent(self, event: QPaintEvent) -> None:
        """Paint the entire widget using the Painter wrapper."""
        with Painter(self, event) as qt_painter:
            self._painter.paint(qt_painter, self.order_handler.labels)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        """Allow dragging the widgets while .acceptDrops() == True."""
        e.accept()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        """Handle all children actions - change order/insert/remove."""
        e.accept()
        source_widget = e.source()

        if not isinstance(source_widget, LabelWidget):
            # Drag incoming from outside the PieWidget ecosystem
            return

        label = source_widget.label
        circle_points = CirclePoints(
            center=self.center,
            radius=self._pie_style.pie_radius)
        distance = circle_points.distance(e.pos())

        if not isinstance(label.value, self._allowed_types):
            # Label type does not match the type of pie menu
            return

        # Remember this widget in case user moves mouse so fast,
        # that there is no other dragMoveEvent to remove it.
        #
        # It will be removed in dragLeaveEvent then.
        self._last_widget = source_widget

        if distance > self._pie_style.widget_radius:
            # Dragged out of the PieWidget
            return self._do(self.order_handler.remove, label)

        if not self.order_handler:
            # First label dragged to empty pie
            return self._do(self.order_handler.append, label)

        if distance < self.deadzone:
            # Do nothing in deadzone
            return

        angle = circle_points.angle_from_point(e.pos())
        label_under_cursor = self.order_handler.label_on_angle(angle)

        if label not in self.order_handler:
            # Dragged with new label, which must be added
            index = self.order_handler.index(label_under_cursor)
            return self._do(self.order_handler.insert, index, label)

        if label_under_cursor == label:
            # Dragged over the same widget
            return

        # Dragged existing label to a new location
        self.order_handler.swap(label_under_cursor, label)

    def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
        """Remove the label when its widget is dragged out."""
        if self._last_widget is not None:
            self._do(self.order_handler.remove, self._last_widget.label)
        return super().dragLeaveEvent(e)

    def reset_size(self) -> None:
        """Set widget geometry according to style."""
        diameter = 2*self._pie_style.widget_radius
        self.setFixedSize(diameter, diameter)

    def _do(self, callback: Callable[..., None], /, *args, **kwargs):
        """Perform callback if changes in values are not restricted."""
        if not self.only_order_change:
            callback(*args, **kwargs)
