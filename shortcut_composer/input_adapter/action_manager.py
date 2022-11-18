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
    def createAction(self, name: str, description: str, menu: str, /)\
        -> QWidgetAction: ...


@dataclass
class ActionContainer:
    plugin_action: PluginAction
    krita_action: QWidgetAction
    shortcut: ShortcutAdapter

    def __post_init__(self):
        """Bind key_press method to action 'trigger' event."""
        self.krita_action.triggered.connect(self.shortcut.on_key_press)


class ActionManager:
    """
    Creates ActionContainers from custom PluginAction and stores them.

    ActionContainer holds all elements of the action being:
    - `PluginAction` implementing the action, used to create the container.
    - `QWidgetAction` recognised by krita, which PluginAction implements.
    - `ShortcutAdapter` which runs proper elements of PluginAction
      interface at proper time.

    Elements other than PluginAction are created and stored in container
    by using the bind_action() method.
    """

    def __init__(self, window: Window):
        self._window = window
        self._event_filter = ReleaseKeyEventFilter()
        self._stored_actions: List[ActionContainer] = []

    def bind_action(self, plugin_action: PluginAction) -> 'ActionContainer':
        """
        Create action components and stores them together.

        The container is stored in internal list to protect it from
        garbage collector.
        """
        container = ActionContainer(
            plugin_action=plugin_action,
            krita_action=self._create_krita_action(plugin_action),
            shortcut=self._create_shortcut_adapter(plugin_action)
        )
        self._stored_actions.append(container)
        return container

    def _create_krita_action(self, plugin_action: PluginAction)\
            -> QWidgetAction:
        """Create QWidgetAction recognised by krita."""
        krita_action = self._window.createAction(
            plugin_action.name,
            plugin_action.name,
            ""
        )
        krita_action.setAutoRepeat(False)
        return krita_action

    def _create_shortcut_adapter(self, action: PluginAction)\
            -> ShortcutAdapter:
        """
        Create ShortcutAdapter which runs elements of PluginAction interface.

        Adapter require registering its callback in event filter.
        """
        shortcut = ShortcutAdapter(action)
        self._event_filter.register_release_callback(
            shortcut.event_filter_callback  # type: ignore
        )
        return shortcut
