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

DEADZONE: Final[int] = 0
"""Amount of pixels a mouse needs to moved for slider to start work."""

FPS_LIMIT: Final[int] = 60
"""Maximum rate of slider refresh. 0 for no limit"""

ICON_RADIUS_SCALE: Final[float] = 1.0

PIE_RADIUS_SCALE: Final[float] = 1.0

PIE_DEADZONE_SCALE: Final[float] = 1.0

PIE_AREA_COLOR: Final[QColor] = QColor(75, 75, 75, 190)

PIE_ACTIVE_COLOR: Final[QColor] = QColor(100, 150, 230, 255)
