from enum import Enum


class DeadzoneStrategy(Enum):
    """
    Enumeration of actions that can be done on deadzone key release.

    Values are strings meant for being displayed in the UI.
    """
    DO_NOTHING = "Do nothing"
    PICK_TOP = "Pick top"
    PICK_PREVIOUS = "Pick previous"
