# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QHBoxLayout,
    QTabWidget,
    QComboBox,
    QWidget,
    QDialog,
)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QCursor

from api_krita import Krita
from .config import Config
from .settings_dialog_utils import (
    ComboBoxesLayout,
    SpinBoxesLayout,
    ButtonsLayout
)


class SettingsDialog(QDialog):
    """Dialog which allows to change global settings of the plugin."""

    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Configure Shortcut Composer")

        self._tab_dict = {
            "General": GeneralSettingsTab(),
            "Pie values": PieValuesTab(),
        }
        tab_holder = QTabWidget()
        for name, tab in self._tab_dict.items():
            tab_holder.addTab(tab, name)

        full_layout = QVBoxLayout(self)
        full_layout.addWidget(tab_holder)
        full_layout.addLayout(ButtonsLayout(
            ok_callback=self.ok,
            apply_callback=self.apply,
            reset_callback=self.reset,
            cancel_callback=self.hide,
        ))
        self.setLayout(full_layout)

    def show(self) -> None:
        """Show the dialog after refreshing all its elements."""
        self.refresh()
        self.move(QCursor.pos())
        return super().show()

    def apply(self) -> None:
        """Ask all dialog zones to apply themselves."""
        for tab in self._tab_dict.values():
            tab.apply()
        Krita.trigger_action("Reload Shortcut Composer")

    def ok(self) -> None:
        """Hide the dialog after applying the changes"""
        self.apply()
        self.hide()

    def reset(self) -> None:
        """Reset all config values to defaults in krita and elements."""
        Config.reset_defaults()
        self.refresh()

    def refresh(self):
        """Ask all tabs to refresh themselves. """
        for tab in self._tab_dict.values():
            tab.refresh()


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


class PieValuesTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()

        self.list_widget = QListWidget(self)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.list_widget.addItems(['ASD', 'ZXC', 'UIO'])

        self.combo_box = QComboBox()
        self.combo_box.addItems(["A", "B", "C"])

        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add)

        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(self.remove)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.combo_box)
        control_layout.addWidget(add_button)
        control_layout.addWidget(remove_button)

        layout.addWidget(self.list_widget)
        layout.addLayout(control_layout)

        self.setLayout(layout)

    def add(self):
        current_row = self.list_widget.currentRow()
        value = self.combo_box.currentText()
        self.list_widget.insertItem(current_row+1, value)
        self.list_widget.setCurrentRow(current_row+1)

    def remove(self):
        current_row = self.list_widget.currentRow()
        self.list_widget.takeItem(current_row)

    def apply(self):
        pass

    def refresh(self):
        pass
