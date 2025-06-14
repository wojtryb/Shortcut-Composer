# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
    QLabel)

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from ..pie_config import PieConfig


class LocationTab(QWidget):
    """PieSettings tab for changing location in which values are saved."""

    def __init__(
        self,
        config: PieConfig,
        parent: QWidget | None = None
    ) -> None:
        """Tab that allows to switch location in which icon order is saved."""
        super().__init__(parent)
        self._config = config

        self._location_button = self._init_location_button()
        self._mode_title = self._init_mode_title()
        self._mode_description = self._init_mode_description()
        self._set_new_default_button = self._init_set_new_default_button()
        self._reset_to_default_button = self._init_reset_to_default_button()

        self._config.register_callback(self._update_button_activity)
        self._update_button_activity()

        self.setLayout(self._init_layout())
        self.is_local_mode = self._config.SAVE_LOCAL.read()

    def _init_layout(self) -> QVBoxLayout:
        """
        Create and set a layout of the tab.

        - Header holds a button for switching save locations.
        - Main area consists of labels describing active location.
        - Footer consists of buttons with additional value management
          actions.
        """
        header = QHBoxLayout()
        header_label = QLabel(text="Change save location:")
        header.addWidget(header_label, 2, Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self._location_button, 1)

        layout = QVBoxLayout()
        layout.addLayout(header)
        layout.addWidget(self._mode_title)
        layout.addWidget(self._mode_description)
        layout.addStretch()
        layout.addWidget(self._set_new_default_button)
        layout.addWidget(self._reset_to_default_button)
        return layout

    def _init_location_button(self) -> SafeConfirmButton:
        """Return button that switches between save locations."""
        def switch_mode() -> None:
            values = self._config.ORDER.read()

            self.is_local_mode = not self.is_local_mode
            if self.is_local_mode:
                self._config.reset_the_default()

            # make sure the icons stay the same
            self._config.ORDER.write(values)

        button = SafeConfirmButton(text="Change mode")
        button.clicked.connect(switch_mode)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_mode_title(self) -> QLabel:
        """Return QLabel with one-line description of the active mode."""
        label = QLabel()
        label.setStyleSheet("font-weight: bold")
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label.setWordWrap(True)
        label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored)
        return label

    def _init_mode_description(self) -> QLabel:
        """Return QLabel with one detailed description of the active mode."""
        label = QLabel()
        label.setWordWrap(True)
        label.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored)
        return label

    def _init_set_new_default_button(self) -> SafeConfirmButton:
        """Return button saving currently active values as the default ones."""
        button = SafeConfirmButton(
            text="Set pie values as a new default",
            icon=Krita.get_icon("document-save"))
        button.clicked.connect(self._config.set_current_as_default)
        button.clicked.connect(self._update_button_activity)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_reset_to_default_button(self) -> SafeConfirmButton:
        """Return button which resets values in pie to default ones."""
        button = SafeConfirmButton(
            text="Reset pie values to default",
            icon=Krita.get_icon("edit-delete"))
        button.clicked.connect(self._config.reset_to_default)
        button.clicked.connect(self._update_button_activity)
        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    @property
    def is_local_mode(self) -> bool:
        """Return whether pie saves the values locally."""
        return self._config.SAVE_LOCAL.read()

    @is_local_mode.setter
    def is_local_mode(self, value: bool) -> None:
        """Return whether pie should save the values locally."""
        if value:
            self._location_button.main_text = "Local"
            self._location_button.icon = Krita.get_icon("folder-documents")
            self._mode_title.setText(
                "Pie values are saved in the .kra document.\n")
            self._mode_description.setText(
                "Each new document starts with the default set of "
                "values which are can to be modified to those used "
                "in given file the most.\n\n"

                "Saved values are not lost between sessions.\n\n"

                "Switching between documents, results in pie switching "
                "the values to those saved in the active document.\n\n"

                "For resources, only resource names are stored. "
                "Saved value will be lost, when the resource is missing.")
        else:
            self._location_button.main_text = "Global"
            self._location_button.icon = Krita.get_icon("properties")
            self._mode_title.setText(
                "Pie values are saved in krita settings.\n")
            self._mode_description.setText(
                "Values remain the same until modified by the user.\n\n"

                "Selected values and their order is saved between "
                "sessions. This mode is meant to be used for values that "
                "remain useful regardless of which document is edited.")
        self._config.SAVE_LOCAL.write(value)

    def _update_button_activity(self) -> None:
        """Disable location action buttons, when they won't do anything."""
        if not self._config.is_order_default():
            self._set_new_default_button.setEnabled(True)
            self._reset_to_default_button.setEnabled(True)
        else:
            self._set_new_default_button.setDisabled(True)
            self._reset_to_default_button.setDisabled(True)
