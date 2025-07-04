# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

try:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QVBoxLayout,
        QHBoxLayout,
        QSizePolicy,
        QWidget,
        QLabel)
except ModuleNotFoundError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QVBoxLayout,
        QHBoxLayout,
        QSizePolicy,
        QWidget,
        QLabel)

from api_krita import Krita
from api_krita.pyqt import SafeConfirmButton
from core_components import Controller
from composer_utils import GroupOrderHolder
from ..pie_config import PieConfig
from ..pie_widget_utils import PieWidgetOrder
from ..pie_label_creator import PieLabelCreator


class TabSaveLocation(QWidget):
    """PieSettings tab for changing location in which values are saved."""

    def __init__(
        self,
        config: PieConfig,
        order_handler: PieWidgetOrder,
        controller: Controller,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._order_handler = order_handler
        self._label_creator = PieLabelCreator(controller)

        self._group_order_holder = GroupOrderHolder(controller.TYPE)
        self._location_button = self._init_location_button()
        self._mode_title = self._init_mode_title()
        self._mode_description = self._init_mode_description()
        self._set_new_default_button = self._init_set_new_default_button()
        self._reset_to_default_button = self._init_reset_to_default_button()

        self._order_handler.register_callback_on_change(self._update_buttons)
        self._config.GROUP_MODE.register_callback(self._update_buttons)
        self._config.GROUP_NAME.register_callback(self._update_buttons)
        self._update_buttons()

        self.setLayout(self._init_layout())
        self.is_local_mode = self._config.SAVE_LOCAL.read()

    def _init_layout(self) -> QVBoxLayout:
        """
        Create and set a layout of the tab.

        - Header holds a button for switching save locations.
        - Main area consists of labels describing active location.
        - Footer consists of buttons for resetting value to default and
          for specifying the new default.
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
            self.is_local_mode = not self.is_local_mode
            if self.is_local_mode:
                self._config.GROUP_MODE.default = False
                self._config.GROUP_NAME.default = ""
                self._config.ORDER.default = []

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
        """Return QLabel with detailed description of the active mode."""
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

        def set_current_as_default():
            self._config.GROUP_MODE.default = self._config.GROUP_MODE.read()
            self._config.GROUP_NAME.default = self._config.GROUP_NAME.read()
            self._config.ORDER.default = self._order_handler.values

        button.clicked.connect(set_current_as_default)
        button.clicked.connect(self._update_buttons)

        button.setFixedHeight(button.sizeHint().height()*2)
        return button

    def _init_reset_to_default_button(self) -> SafeConfirmButton:
        """Return button which resets values in pie to default ones."""
        button = SafeConfirmButton(
            text="Reset pie values to default",
            icon=Krita.get_icon("edit-delete"))

        def reset_order_to_default():
            self._config.GROUP_MODE.reset_default()
            self._config.GROUP_NAME.reset_default()
            self._config.ORDER.reset_default()

            labels = self._label_creator.labels_from_config(self._config)
            self._order_handler.replace_labels(labels)

        button.clicked.connect(reset_order_to_default)
        button.clicked.connect(self._update_buttons)

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

    def _update_buttons(self) -> None:
        """Disable location action buttons, when they won't do anything."""
        cfg = self._config
        if not cfg.GROUP_MODE.read():
            is_order_default = (
                cfg.GROUP_MODE.read() == cfg.GROUP_MODE.default
                and cfg.GROUP_NAME.read() == cfg.GROUP_NAME.default
                and self._order_handler.values == cfg.ORDER.default)
        else:
            is_order_default = cfg.GROUP_NAME.read() == cfg.GROUP_NAME.default

        if not is_order_default:
            self._set_new_default_button.setEnabled(True)
            self._reset_to_default_button.setEnabled(True)
        else:
            self._set_new_default_button.setDisabled(True)
            self._reset_to_default_button.setDisabled(True)
