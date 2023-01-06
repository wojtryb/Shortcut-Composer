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
    def createAction(name: str, description: str, menu: str, /)\
        -> QWidgetAction: ...


class ActionManager:
    """
    Creates and stores plugin action containers.

    Stores each custom plugin action with its newly created components:
    shortcut binding and krita action.
    """

    @dataclass
    class ActionContainer:
        plugin_action: PluginAction
        krita_action: QWidgetAction
        shortcut: ShortcutAdapter

        def __post_init__(self):
            """Bind key_press method to action 'trigger' event."""
            self.krita_action.triggered.connect(self.shortcut.on_key_press)

    def __init__(self, window: Window):
        self._window = window
        self._event_filter = ReleaseKeyEventFilter()
        self._stored_actions: List[self.ActionContainer] = []

    def bind_action(self, plugin_action: PluginAction) -> 'ActionContainer':
        """
        Store objects needed for creating action components:

        - krita window -- on which krita actions are created
        - event filter -- to which they are connected
        - stored_actions -- list that protects all actions from garbage
          collector.
        """
        container = self.ActionContainer(
            plugin_action=plugin_action,
            krita_action=self._create_krita_action(plugin_action),
            shortcut=self._create_shortcut_adapter(plugin_action)
        )
        self._stored_actions.append(container)
        return container

    def _create_krita_action(self, plugin_action: PluginAction)\
            -> QWidgetAction:
        krita_action = self._window.createAction(
            plugin_action.name,
            plugin_action.name,
            ""
        )
        krita_action.setAutoRepeat(False)
        return krita_action

    def _create_shortcut_adapter(self, action: PluginAction)\
            -> ShortcutAdapter:
        shortcut = ShortcutAdapter(action)
        self._event_filter.register_release_callback(
            shortcut.event_filter_callback)
        return shortcut
