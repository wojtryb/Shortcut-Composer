# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The only python file directly run by krita during plugin init phase.

Checks whether plugin requirements are met and aborts the start if not.
"""
import sys
import os

# Appending this file location to python PATH allows to directly import
# main packages instead of using relative imports.
sys.path.append(directory := os.path.dirname(__file__))


def main() -> None:
    # Failing to import PyQt5 package most likely means krita 6 is used.
    # Krita 6 uses PyQt6 which is not supported in this version.
    #
    # In that case, display a message and abort plugin start.
    try:
        from PyQt5.QtWidgets import QMessageBox
        from PyQt5.QtCore import Qt
    except ModuleNotFoundError:
        from PyQt6.QtWidgets import QMessageBox
        from PyQt6.QtCore import Qt

    from .INFO import __version__, __required_krita_version__
    from .api_krita import Krita

    # If krita version is known and too low, abort the plugin start
    # If krita version is unknown (built from source), assume it is correct
    if Krita.version.is_known and Krita.version < __required_krita_version__:
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Icon.Warning)
        warning_box.setWindowTitle("Shortcut composer version mismatch")
        warning_box.setTextFormat(Qt.TextFormat.RichText)
        warning_box.setText(
            "Shortcut Composer will not load.<br><br>"
            f"The plugin in version {__version__} requires higher "
            "Krita version.<br><br>"
            f"Krita version: {Krita.version}<br>"
            f"Required Krita version: {__required_krita_version__}<br><br>"
            "Upgrade your Krita, or downgrade the plugin.")
        warning_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        warning_box.exec()
        return

    from .shortcut_composer import ShortcutComposer  # noqa
    Krita.add_extension(ShortcutComposer)


main()
