# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from .config_based_widget import ConfigBasedWidget
from .config_form_widget import ConfigFormWidget
from .widgets import ConfigComboBox, ConfigSpinBox

__all__ = [
    "ConfigBasedWidget",
    "ConfigFormWidget",
    "ConfigComboBox",
    "ConfigSpinBox"
]
