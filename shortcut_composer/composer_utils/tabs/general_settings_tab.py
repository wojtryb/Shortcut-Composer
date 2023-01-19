# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from ..layouts import (
    ComboBoxesLayout,
    SpinBoxesLayout,
)


class GeneralSettingsTab(QWidget):
    """Dialog which allows to change global settings of the plugin."""

    def __init__(self) -> None:
        super().__init__()

        self._layouts_dict = {
            "ComboBoxes": ComboBoxesLayout(),
            "SpinBoxes": SpinBoxesLayout(),
        }
        full_layout = QVBoxLayout()
        for layout in self._layouts_dict.values():
            full_layout.addLayout(layout)
        self.setLayout(full_layout)

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        for layout in self._layouts_dict.values():
            layout.apply()

    def refresh(self) -> None:
        """Ask all dialog zones to refresh themselves. """
        for layout in self._layouts_dict.values():
            layout.refresh()
