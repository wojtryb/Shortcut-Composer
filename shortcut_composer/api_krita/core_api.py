# SPDX-FileCopyrightText: © 2022-2023 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from krita import Krita as Api, Extension, qApp
from typing import Callable, Protocol, Any, Dict, Optional

from PyQt5.QtWidgets import (
    QMainWindow,
    QDesktopWidget,
    QWidgetAction,
    QMdiArea)
from PyQt5.QtGui import QKeySequence, QColor, QIcon
from PyQt5.QtCore import QTimer

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
        self.main_window: Any = None

    def get_active_view(self) -> View:
        """Return wrapper of krita `View`."""
        return View(self.instance.activeWindow().activeView())

    def get_active_document(self) -> Optional[Document]:
        """Return wrapper of krita `Document`."""
        document = self.instance.activeDocument()
        if document is None:
            return None
        return Document(document)

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

    def get_presets(self) -> Dict[str, Any]:
        """Return a list of unwrapped preset objects"""
        return self.instance.resources('preset')

    def get_active_qwindow(self) -> QMainWindow:
        """Return qt window of krita. Don't use on plugin init phase."""
        return self.instance.activeWindow().qwindow()

    def get_active_mdi_area(self) -> QMdiArea:
        return self.get_active_qwindow().findChild(QMdiArea)  # type: ignore

    def get_icon(self, icon_name: str) -> QIcon:
        return self.instance.icon(icon_name)

    def read_setting(
        self,
        group: str,
        name: str,
        default: str = "Not stored"
    ) -> Optional[str]:
        """
        Read a setting from kritarc file.

        - Return string red from file if present
        - Return default if it was given
        - Return None if default was not given
        """
        red_value = self.instance.readSetting(group, name, default)
        return None if red_value == "Not stored" else red_value

    def write_setting(self, group: str, name: str, value: Any) -> None:
        """Write setting to kritarc file. Value type will be lost."""
        self.instance.writeSetting(group, name, str(value))

    def create_action(
        self,
        window: 'KritaWindow',
        name: str,
        group: str = "",
        callback: Callable[[], None] = lambda: None
    ) -> QWidgetAction:
        """
        Create a new action in krita.

        Requires providing a krita window received in createActions()
        method of the main extension file.
        """
        krita_action = window.createAction(name, name, group)
        krita_action.setAutoRepeat(False)
        krita_action.triggered.connect(callback)
        return krita_action

    def add_extension(self, extension: Extension) -> None:
        """Add extension/plugin/add-on to krita."""
        self.instance.addExtension(extension(self.instance))

    def add_theme_change_callback(self, callback: Callable[[], None]) -> Any:
        """
        Add method which should be run after the theme is changed.

        Method is delayed with a timer to allow running it on plugin
        initialization phase.
        """
        def connect_callback():
            self.main_window = self.instance.activeWindow()
            if self.main_window is not None:
                self.main_window.themeChanged.connect(callback)
        QTimer.singleShot(1000, connect_callback)

    @property
    def is_light_theme_active(self) -> bool:
        """Return if currently set theme is light using it's main color."""
        main_color: QColor = qApp.palette().window().color()
        return main_color.value() > 128


class KritaWindow(Protocol):
    """Krita window received in createActions() of main extension file."""

    def createAction(
        self,
        name: str,
        description: str,
        menu: str, /
    ) -> QWidgetAction: ...
