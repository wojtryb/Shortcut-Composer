from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidgetAction
from PyQt5.QtGui import QKeySequence
from typing import Callable, Protocol
from krita import Krita as Api, Extension

from .wrappers import (
    ToolDescriptor,
    Document,
    Canvas,
    Cursor,
    View,
)


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    active_tool = ToolDescriptor()
    """Settable property which lets to set and get active tool from toolbox."""

    def __init__(self) -> None:
        self.instance = Api.instance()
        self.screen_size = QDesktopWidget().screenGeometry(-1).width()

    def get_active_view(self) -> View:
        """Return wrapper of krita `View`."""
        return View(self.instance.activeWindow().activeView())

    def get_active_document(self) -> Document:
        """Return wrapper of krita `Document`."""
        return Document(self.instance.activeDocument())

    def get_active_canvas(self) -> Canvas:
        """Return wrapper of krita `Canvas`."""
        return Canvas(self.instance.activeWindow().activeView().canvas())

    def get_cursor(self) -> Cursor:
        """Return wrapper of krita `Cursor`. Don't use on plugin init phase."""
        qwin = self.get_active_qwindow()
        return Cursor(qwin)

    def trigger_action(self, action_name: str) -> None:
        """Trigger internal krita action called `action_name`."""
        return self.instance.action(action_name).trigger()

    def get_action_shortcut(self, action_name: str) -> QKeySequence:
        """Return shortcut of krita action called `action_name`."""
        return self.instance.action(action_name).shortcut()

    def get_presets(self) -> dict:
        """Return a list of unwrapped preset objects"""
        return self.instance.resources('preset')

    def get_active_qwindow(self) -> QMainWindow:
        """Return qt window of krita. Don't use on plugin init phase."""
        return self.instance.activeWindow().qwindow()

    def read_setting(self, group: str, name: str, default: str) -> str:
        return self.instance.readSetting(group, name, default)

    def write_setting(self, group: str, name: str, value: str) -> None:
        self.instance.writeSetting(group, name, value)

    def create_action(
        self,
        window: 'KritaWindow',
        name: str,
        group: str = "",
        callback: Callable[[], None] = lambda: None
    ):
        krita_action = window.createAction(name, name, group)
        krita_action.setAutoRepeat(False)
        krita_action.triggered.connect(callback)
        return krita_action

    def add_extension(self, extension: Extension) -> None:
        """Add extension/plugin/add-on to krita."""
        self.instance.addExtension(extension(self.instance))


class KritaWindow(Protocol):
    def createAction(
        self,
        name: str,
        description: str,
        menu: str, /
    ) -> QWidgetAction: ...
