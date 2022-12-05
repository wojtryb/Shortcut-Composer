"""
Defines global, default values for action templates.

Used, when no specific per-action configuration is given.
"""

from typing import Final


SHORT_VS_LONG_PRESS_TIME: Final[float] = 0.3
"""Time in seconds distinguishing short key presses from long ones."""

PIXELS_IN_UNIT: Final[int] = 50
"""Amount of pixels a mouse needs to be moved for slider to change by 1.0"""

DEADZONE: Final[int] = 0
"""Amount of pixels a mouse needs to moved for slider to start work."""

FPS_LIMIT: Final[int] = 60
"""Maximum rate of slider refresh. 0 for no limit"""

PIE_ICON_RADIUS_PX: Final[int] = 50

PIE_RADIUS_PX: Final[int] = 165
