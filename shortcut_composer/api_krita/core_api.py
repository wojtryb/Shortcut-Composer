from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QKeySequence
from krita import Krita as Api, Extension

from .wrappers import (
    ToolDescriptor,
    Document,
    Canvas,
    Cursor,
    View,
)
from .enums import Toggle


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    active_tool = ToolDescriptor()
    """Settable property which lets to set and get active tool from toolbox."""

    def __init__(self) -> None:
        self.instance = Api.instance()

    def get_active_view(self) -> View:
        """Return wrapper of krita `View`."""
        return View(self.instance.activeWindow().activeView())

    def get_cursor(self) -> Cursor:
        """Return wrapper of krita `Cursor`. Don't use on plugin init phase."""
        qwin = self.get_active_qwindow()
        return Cursor(qwin)

    def get_active_document(self) -> Document:
        """Return wrapper of krita `Document`."""
        return Document(self.instance.activeDocument())

    def get_active_canvas(self) -> Canvas:
        """Return wrapper of krita `Canvas`."""
        return Canvas(self.instance.activeWindow().activeView().canvas())

    def trigger_action(self, action_name: str) -> None:
        """Trigger internal krita action called `action_name`."""
        return self.instance.action(action_name).trigger()

    def get_action_shortcut(self, action_name: str) -> QKeySequence:
        """Return shortcut of krita action called `action_name`."""
        return self.instance.action(action_name).shortcut()

    def get_toggle_state(self, toggle: Toggle) -> bool:
        """Return state of checkable krita action called `action_name`."""
        return self.instance.action(toggle.value).isChecked()

    def set_toggle_state(self, toggle: Toggle, state: bool) -> None:
        """Set state of checkable krita action (toggle) by its enum."""
        return self.instance.action(toggle.value).setChecked(state)

    def get_presets(self) -> dict:
        """Return a list of unwrapped preset objects"""
        return self.instance.resources('preset')

    def get_active_qwindow(self) -> QMainWindow:
        """Return qt window of krita. Don't use on plugin init phase."""
        return self.instance.activeWindow().qwindow()

    def add_extension(self, extension: Extension) -> None:
        """Add extension/plugin/add-on to krita."""
        self.instance.addExtension(extension(self.instance))
