# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Required part of api_krita package, so that no dependency is needed."""

from krita import Krita as Api
from typing import Callable, Protocol

from PyQt5.QtWidgets import QWidgetAction
from PyQt5.QtGui import QKeySequence


class KritaWindow(Protocol):
    """Krita window received in createActions() of main extension file."""

    def createAction(
        self,
        name: str,
        description: str,
        menu: str, /
    ) -> QWidgetAction: ...


class KritaInstance:
    """Wraps krita API for typing, documentation and PEP8 compatibility."""

    def __init__(self) -> None:
        self.instance = Api.instance()

    def get_action_shortcut(self, action_name: str) -> QKeySequence:
        """Return shortcut of krita action called `action_name`."""
        return self.instance.action(action_name).shortcut()

    def create_action(
        self,
        window: KritaWindow,
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


Krita = KritaInstance()
