# SPDX-FileCopyrightText: © 2022-2026 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The only python file directly run by krita during plugin init phase.

Checks whether plugin requirements are met and aborts the start if not.
"""
import sys
import os
import platform
from pathlib import Path

# Appending this file location to python PATH allows to directly import
# main packages instead of using relative imports.
sys.path.append(directory := os.path.dirname(__file__))


def main() -> None:
    from PyQt.QtWidgets import QMessageBox
    from PyQt.QtCore import Qt

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

    # On Windows, since krita 6 transparent Qt widgets are rendered black
    # unless canvas is rendered with OpenGL, or the acceleration is disabled
    # Show a warning message on startup when this situation is detected
    if platform.system() == "Windows" and Krita.version.major >= 6:
        warning_needed = True
        try:
            with open(Path.home()/"AppData"/"Local"/"kritadisplayrc") as f:
                text = f.read()
                if "OpenGLRenderer=desktop" in text \
                        or "OpenGLRenderer=none" in text:
                    warning_needed = False
        except OSError:
            pass

        if warning_needed:
            warning_box = QMessageBox()
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setWindowTitle("Warning: OpenGL is not being used")
            warning_box.setTextFormat(Qt.TextFormat.RichText)
            warning_box.setText(
                "Shortcut Composer detected that OpenGL is not being used.<br>"
                "This may result in transparency issues.<br>"
                "Please, change renderer to OpenGL in:<br><br>"
                "Settings > Configure Krita > Display > Canvas Acceleration"
                "<br><br>Then, restart krita.")
            warning_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            warning_box.exec()

    from .shortcut_composer import ShortcutComposer  # noqa
    Krita.add_extension(ShortcutComposer)


main()
