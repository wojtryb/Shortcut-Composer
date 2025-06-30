# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Callable

from PyQt5.QtGui import QCursor

from api_krita.pyqt import Timer
from composer_utils import CirclePoints, Config
from data_components import PieDeadzoneStrategy
from .pie_label import PieLabel
from .pie_widget import PieWidget


class PieLabelSelector:
    """
    Handles the passed PieWidget by tracking a mouse to select a label.

    - Starts tracking on `start()`, and ensures the pie is shown under
      the cursor.
    - During tracking, marks the label under the cursor as selected.
    - Starts the label animation each time new label is selected
    - Stops tracking on `stop()`.

    Tracking is done by timer that calls `_handle_cursor` repeatedly.

    Selected label is stored in public attribute, which can be None,
    when no label was selected.
    """
    """
    Selects label from the pie based on marked ...
    Activates the correct labels from the Pie.

    TODO update dosctring and class name

    When a valid label is given in `activate()` method, it us activated
    and also remembered.

    When label is not given in `activate()` method, it means that user
    closed the pie while still being in deadzone.
    Then it is handled using the currently active strategy.

    Actuator tracks selected strategy using `strategy_field` passed on
    initialization. It can be changed in runtime.
    """

    def __init__(
        self,
        pie_widget: PieWidget,
        initial_label: PieLabel | None = None,
        initial_strategy: PieDeadzoneStrategy = PieDeadzoneStrategy.DO_NOTHING,
    ) -> None:
        self._pie_widget = pie_widget
        self._previous_label = initial_label

        self.strategy = initial_strategy

        self._hovered_label: PieLabel | None = None
        self._timer = Timer(self._handle_cursor, Config.get_sleep_time())
        self._animator = _LabelAnimator(
            pie_widget=pie_widget,
            hovered_label_callback=lambda: self._hovered_label)

    def start_tracking(self) -> None:
        """Show widget under the mouse and start the mouse tracking loop."""
        self._pie_widget.move_center(QCursor().pos())
        self._pie_widget.show()

        self._mark_suggested_widget()
        self._timer.start()

        # Make sure the pie widget is not draggable. It could have been
        # broken by pie settings reloading the widgets.
        self._pie_widget.draggable = False

    def stop_tracking(self) -> None:
        """Stop the mouse tracking loop and reset internal label values."""
        self._hovered_label = None
        self._timer.stop()
        for label in self._pie_widget.order_handler:
            label.activation_progress.reset()
        self._unmark_all_widgets()

    def select(self) -> PieLabel | None:
        # Out of deadzone, label picked
        if self._hovered_label is not None:
            self._previous_label = self._hovered_label
            return self._hovered_label

        # In deadzone, use strategy to select label
        return self._label_from_strategy()

    def _label_from_strategy(self) -> PieLabel | None:
        """Return label suggested by current strategy."""
        labels = self._pie_widget.order_handler.labels

        match self.strategy:
            case PieDeadzoneStrategy.PICK_TOP:
                if labels:
                    return labels[0]
            case PieDeadzoneStrategy.PICK_PREVIOUS:
                if self._previous_label in labels:
                    return self._previous_label
        return None

    def _handle_cursor(self) -> None:
        """Calculate zone of the cursor and mark which child is selected."""
        # NOTE: The widget can get hidden outside of stop() when key is
        # released during the drag&drop operation or when user clicked
        # outside the pie widget.
        if not self._pie_widget.isVisible():
            self._pie_widget.hide()
            return self.stop_tracking()

        if self._pie_widget.acceptDrops():
            return self.stop_tracking()

        if not self._pie_widget.order_handler:
            return

        cursor = QCursor().pos()
        circle = CirclePoints(self._pie_widget.center_global, 0)
        if circle.distance(cursor) < self._pie_widget.deadzone:
            return self._update_hovered(None)

        angle = circle.angle_from_point(cursor)
        handler = self._pie_widget.order_handler
        self._update_hovered(handler.label_on_angle(angle))

    def _update_hovered(self, label: PieLabel | None) -> None:
        """Mark label as selected and start animating the change."""
        if self._hovered_label != label:
            self._hovered_label = label
            self._animator.start()

    def _mark_suggested_widget(self) -> None:
        """Force color of the label that is selected for being picked."""
        self._unmark_all_widgets()

        label = self._label_from_strategy()
        if label is None:
            return

        if label in self._pie_widget.order_handler.labels:
            widget = self._pie_widget.order_handler.widget_with_label(label)
            widget.forced = True

    def _unmark_all_widgets(self):
        for widget in self._pie_widget.order_handler.widgets:
            widget.forced = False


class _LabelAnimator:
    """
    Controls the animation of background under pie labels.

    Handles the whole widget at once, to prevent unnecessary repaints.
    """

    def __init__(
        self,
        pie_widget: PieWidget,
        hovered_label_callback: Callable[[], PieLabel | None]
    ) -> None:
        self._pie_widget = pie_widget
        self._hovered_label_callback = hovered_label_callback
        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self) -> None:
        """Start animating. The animation will stop automatically."""
        self._timer.start()

    def _update(self) -> None:
        """Move all labels to next animation state. End animation if needed."""
        for label in self._pie_widget.order_handler:
            if self._hovered_label_callback() == label:
                label.activation_progress.up()
            else:
                label.activation_progress.down()

        self._pie_widget.repaint()
        for label in self._pie_widget.order_handler:
            if label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
