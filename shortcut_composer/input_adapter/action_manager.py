"""
Module binding custom action objects to krita's key_press actions and
key_release events.
"""

from dataclasses import dataclass
from typing import List, Protocol

from PyQt5.QtWidgets import QWidgetAction

from .plugin_action import PluginAction
from .event_filter import ReleaseKeyEventFilter
from .shortcut_adapter import ShortcutAdapter


class Window(Protocol):
    def createAction(name: str, description: str, menu: str, /) -> None: ...


class ActionManager:
    """
    Creates and stores plugin action containers.

    Stores each custom plugin action with its newly created components:
    shortcut binding and krita action.
    """

    @dataclass
    class ActionContainer:
        """
        Holds action components:

        action -- contains logic to perform on CUSTOM key events
        krita_action -- krita/Qt5 action object visible in krita settings
        shortcut -- maps krita key events to custom ones
        """

        action: PluginAction
        krita_action: QWidgetAction
        shortcut: ShortcutAdapter

        def __post_init__(self):
            """Bind key_press method to action 'trigger' event."""
            self.krita_action.setAutoRepeat(False)
            self.krita_action.triggered.connect(self.shortcut.on_key_press)

    def __init__(self, window: Window):
        """
        Store objects needed for creating action components:

        - krita window -- on which krita actions are created
        - event filter -- to which they are connected
        - stored_actions -- list that protects all actions from garbage
          collector.
        """
        self._window = window
        self._event_filter = ReleaseKeyEventFilter()
        self._stored_actions: List[self.ActionContainer] = []

    def bind_action(self, action: PluginAction) -> 'ActionContainer':
        """Creates action components and stores them together."""
        krita_action: QWidgetAction = self._window.createAction(
            action.action_name,
            action.action_name,
            ""
        )
        shortcut = ShortcutAdapter(action)
        self._event_filter.register_release_callback(
            shortcut.event_filter_callback)

        container = self.ActionContainer(action, krita_action, shortcut)
        self._stored_actions.append(container)

        return container
