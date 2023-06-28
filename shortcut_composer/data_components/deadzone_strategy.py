from enum import Enum


class DeadzoneStrategy(Enum):
    DO_NOTHING = "Do nothing"
    ACTIVATE_TOP = "Activate top"
    ACTIVATE_LAST = "Activate last"
