# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Union
from PyQt5.QtGui import QPixmap, QIcon
from api_krita.pyqt import Text


class Controller:
    """Component that allows to get and set a specific property of krita."""

    default_value: Any = None

    def refresh(self) -> None: """Refresh stored krita components."""
    def get_value(self) -> Any: """Get handled value from krita."""
    def set_value(self, value: Any) -> None: """Set handled value in krita."""
    def get_label(self, value: Any) -> Union[Text, QPixmap, QIcon, None]: ...
