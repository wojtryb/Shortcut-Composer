"""
Defines global, default values for action templates.

Used, when no specific per-action configuration is given.
"""

from PyQt5.QtGui import QColor
from typing import Final


SHORT_VS_LONG_PRESS_TIME: Final[float] = 0.3
"""Time in seconds distinguishing short key presses from long ones."""

PIXELS_IN_UNIT: Final[int] = 50
"""Amount of pixels a mouse needs to be moved for slider to change by 1.0"""

SLIDER_DEADZONE: Final[int] = 0
"""Amount of pixels a mouse needs to moved for slider to start work."""

FPS_LIMIT: Final[int] = 60
"""Maximum rate of slider refresh. 0 for no limit"""

PIE_RADIUS_GLOBAL_SCALE: Final[float] = 1.0
"""Global scale factor for all the pie menus."""

ICON_RADIUS_GLOBAL_SCALE: Final[float] = 1.0
"""Global scale factor for all the pie menu icons."""

PIE_DEADZONE_GLOBAL_SCALE: Final[float] = 1.0
"""Global scale factor for all the deadzone areas in pie menus."""

PIE_BACKGROUND_COLOR: Final[QColor] = QColor(75, 75, 75, 190)
"""Default background color of all the pie menus without explicit one."""

PIE_ACTIVE_COLOR: Final[QColor] = QColor(100, 150, 230, 255)
"""Default color of active pie menu icon when there is no explicit one."""
