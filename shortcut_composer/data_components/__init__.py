# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Contains data components available for user to configure shortcuts.

Data components are meant to provide easy configuration format.
They can perform simple operations in krita, but shouldn't hold any
complex logic.
"""

from .strategies import (
    RotationDeadzoneStrategy,
    PieDeadzoneStrategy,
    PickLayerStrategy)
from .current_layer_stack import CurrentLayerStack
from .slider import Slider
from .range import Range
from .group import Group

__all__ = [
    "RotationDeadzoneStrategy",
    "PieDeadzoneStrategy",
    "PickLayerStrategy",
    "CurrentLayerStack",
    "Slider",
    "Range",
    "Group"]
