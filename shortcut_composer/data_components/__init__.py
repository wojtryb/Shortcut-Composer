# SPDX-FileCopyrightText: © 2022 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Contains data components available for user to configure shortcuts.

Data components are meant to provide easy configuration format.
They can perform simple operations in krita, but shouldn't hold any
complex logic.
"""

from .current_layer_stack import CurrentLayerStack
from .pick_strategy import PickStrategy
from .slider import Slider
from .range import Range
from .tag import Tag

__all__ = [
    "CurrentLayerStack",
    "PickStrategy",
    "Slider",
    "Range",
    "Tag",
]
