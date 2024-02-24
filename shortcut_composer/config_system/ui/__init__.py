# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
UI elements based on the config concept introduced in parent package.

Grants QWidgets paired with configuration fields.
All widgets have unified interface for reading and setting their values.

They also allow to directly fill them with values from kritarc, save
their current values to kritarc, and reset them to default values of
fields they hold.

ConfigFormWidget is a class that aggregates multiple input widgets,
display them in a form, and allow to perform actions with all of them at
once using their unified interface.
"""

from .config_based_widget import ConfigBasedWidget
from .config_form_widget import ConfigFormWidget
from .widgets import (
    StringComboBox,
    EnumComboBox,
    ColorButton,
    Checkbox,
    SpinBox)

__all__ = [
    "ConfigBasedWidget",
    "ConfigFormWidget",
    "StringComboBox",
    "EnumComboBox",
    "ColorButton",
    "Checkbox",
    "SpinBox"]
