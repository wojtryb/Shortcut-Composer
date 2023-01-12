from api_krita.pyqt import Timer
from .pie_widget import PieWidget


class LabelAnimator:
    """
    Controls the animation of background under pie labels.

    Handles the whole widget at once, to prevent unnecessary repaints.
    """

    def __init__(self, widget: PieWidget) -> None:
        self._widget = widget
        self._labels = widget.labels
        self._timer = Timer(self._update, 17)

    def start(self):
        """Start animating. The animation will stop automatically."""
        self._timer.start()

    def _update(self):
        """Move all labels to next animation state. End animation if needed."""
        for label in self._labels:
            if self._labels.active == label:
                label.activation_progress.up()
            else:
                label.activation_progress.down()

        self._widget.repaint()
        for label in self._labels:
            if label.activation_progress.value not in (0, 1):
                return
        self._timer.stop()
