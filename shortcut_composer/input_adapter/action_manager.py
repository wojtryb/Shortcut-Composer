# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module binding custom action objects to krita's key_press actions and
key_release events.
"""

from dataclasses import dataclass

from PyQt5.QtWidgets import QWidgetAction

from .action_manager_utils import Krita, ReleaseKeyEventFilter, ShortcutAdapter
from .complex_action_interface import ComplexActionInterface


@dataclass
class ActionContainer:
    """
    Holds action elements together.

    - `ComplexActionInterface` is the action implementation.
    - `QWidgetAction` krita representation, which ComplexAction implements.
    - `ShortcutAdapter` manages running elements of ComplexAction
      interface at right time.
    """
    core_action: ComplexActionInterface
    krita_action: QWidgetAction
    shortcut: ShortcutAdapter

    def __post_init__(self) -> None:
        """Bind key_press method to action 'trigger' event."""
        self.krita_action.triggered.connect(self.shortcut.on_key_press)

    def replace_action(self, new_action: ComplexActionInterface) -> None:
        """Replace plugin action managed by this container."""
        self.core_action = new_action
        self.shortcut.action = new_action


class ActionManager:
    """
    Creates and stores `ActionContainers` from `ComplexActionInterfaces`.

    Ensures, that methods of the action interface will be called at
    appropriate keyboard input events.

    `QWidgetAction` and `ShortcutAdapter` are created and stored in
    container along with passed `ComplexActionInterfaces` by using the
    bind_action() method.
    """

    def __init__(self, window) -> None:
        self._window = window
        self._event_filter = ReleaseKeyEventFilter()
        self._stored_actions: dict[str, ActionContainer] = {}

    def bind_action(self, action: ComplexActionInterface) -> None:
        """
        Create action components and stores them together.

        The container is stored in internal list to protect it from
        garbage collector.
        """
        if action.name in self._stored_actions:
            self._stored_actions[action.name].replace_action(action)
            return

        container = ActionContainer(
            core_action=action,
            krita_action=Krita.create_action(
                window=self._window,
                name=action.name),
            shortcut=self._create_adapter(action))

        self._stored_actions[action.name] = container

    def _create_adapter(self, action: ComplexActionInterface) \
            -> ShortcutAdapter:
        """
        Create ShortcutAdapter which runs elements of ComplexAction interface.

        Adapter require registering its callback in event filter.
        """
        shortcut_adapter = ShortcutAdapter(action)
        self._event_filter.register_release_callback(
            shortcut_adapter.event_filter_callback)  # type: ignore
        return shortcut_adapter
