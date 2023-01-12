# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
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
        layout = QVBoxLayout()
        for layout_part in self._layouts_dict.values():
            layout.addLayout(layout_part)

        stretched = QHBoxLayout()
        stretched.addStretch()
        stretched.addLayout(layout)
        stretched.addStretch()
        self.setLayout(stretched)

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        for layout in self._layouts_dict.values():
            layout.apply()

    def refresh(self) -> None:
        """Ask all dialog zones to refresh themselves. """
        for layout in self._layouts_dict.values():
            layout.refresh()
