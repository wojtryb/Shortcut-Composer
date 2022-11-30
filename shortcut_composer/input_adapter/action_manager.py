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


@dataclass
class ActionContainer:
    """
    Holds action elements together.

    - `PluginAction` is the action implementation.
    - `QWidgetAction` krita representation, which PluginAction implements.
    - `ShortcutAdapter` manages running elements of PluginAction
      interface at right time.

    """
    plugin_action: PluginAction
    krita_action: QWidgetAction
    shortcut: ShortcutAdapter

    def __post_init__(self):
        """Bind key_press method to action 'trigger' event."""
        self.krita_action.triggered.connect(self.shortcut.on_key_press)


class ActionManager:
    """
    Creates and stores `ActionContainers` from `PluginActions`.

    `QWidgetAction` and `ShortcutAdapter` are created and stored in
    container along with passed `PluginAction` by using the
    bind_action() method.
    """

    class Window(Protocol):
        def createAction(
            self,
            name: str,
            description: str,
            menu: str, /
        ) -> QWidgetAction: ...

    def __init__(self, window: Window):
        self._window = window
        self._event_filter = ReleaseKeyEventFilter()
        self._stored_actions: List[ActionContainer] = []

    def bind_action(self, action: PluginAction) -> 'ActionContainer':
        """
        Create action components and stores them together.

        The container is stored in internal list to protect it from
        garbage collector.
        """
        container = ActionContainer(
            plugin_action=action,
            krita_action=self._create_krita_action(action),
            shortcut=self._create_adapter(action)
        )
        self._stored_actions.append(container)
        return container

    def _create_krita_action(self, action: PluginAction) -> QWidgetAction:
        """Create QWidgetAction recognised by krita."""
        krita_action = self._window.createAction(
            action.name,
            action.name,
            ""
        )
        krita_action.setAutoRepeat(False)
        return krita_action

    def _create_adapter(self, action: PluginAction) -> ShortcutAdapter:
        """
        Create ShortcutAdapter which runs elements of PluginAction interface.

        Adapter require registering its callback in event filter.
        """
        shortcut = ShortcutAdapter(action)
        self._event_filter.register_release_callback(
            shortcut.event_filter_callback  # type: ignore
        )
        return shortcut
