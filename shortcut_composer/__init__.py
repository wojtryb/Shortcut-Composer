# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
The only python file directly run by krita during plugin init phase.

Runs the file with extension by importing everything from it.

Appending this file location to python PATH allows to directly import
main packages instead of using relative imports.
"""
import sys
import os

sys.path.append(directory := os.path.dirname(__file__))


def main() -> None:
    from PyQt5.QtWidgets import QMessageBox
    from .INFO import __version__, __required_krita_version__
    from .api_krita import Krita  # noqa

    if Krita.version < __required_krita_version__:
        warning_box = QMessageBox()
        warning_box.setIcon(QMessageBox.Warning)
        warning_box.setWindowTitle("Shortcut composer version mismatch")
        warning_box.setText(
            "Shortcut Composer will not load.\n\n"
            f"The plugin in version {__version__} requires higher "
            "Krita version:\n\n"
            f"Krita version: {Krita.version}\n"
            f"Required Krita version: {__required_krita_version__}\n\n"
            "Upgrade your Krita, or downgrade the plugin.")
        warning_box.setStandardButtons(QMessageBox.Ok)
        warning_box.exec_()
        return

    from .shortcut_composer import ShortcutComposer  # noqa
    Krita.add_extension(ShortcutComposer)


main()
