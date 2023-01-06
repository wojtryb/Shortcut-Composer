"""
Contains data components available for user to configure shortcuts.

Data components are meant to provide easy configuration format.
They can perform simple operations in krita, but shouldn't hold any
complex logic.
"""

from .current_layer_stack import CurrentLayerStack
from .pick_strategy import PickStrategy
from .read_setting import read_setting
from .slider import Slider
from .range import Range
from .tag import Tag

__all__ = [
    "CurrentLayerStack",
    "PickStrategy",
    "read_setting",
    "Slider",
    "Range",
    "Tag",
]
