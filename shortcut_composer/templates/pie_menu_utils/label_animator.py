from api_krita.pyqt import Timer
from .pie_widget import PieWidget

from composer_utils import Config


class LabelAnimator:
    """
    Controls the animation of background under pie labels.

    Handles the whole widget at once, to prevent unnecessary repaints.
    """

    def __init__(self, widget: PieWidget) -> None:
        self._widget = widget
        self._children = widget.widget_holder
        self._timer = Timer(self._update, Config.get_sleep_time())

    def start(self):
        """Start animating. The animation will stop automatically."""
        self._timer.start()

    def _update(self):
        """Move all labels to next animation state. End animation if needed."""
        for widget in self._children:
            if self._children.active == widget:
                widget.label.activation_progress.up()
            else:
                widget.label.activation_progress.down()

        self._widget.repaint()
        for widget in self._children:
            if widget.label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
