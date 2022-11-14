from typing import Any, NewType


MouseInput = NewType("MouseInput", int)
"""Integer returned by krita with a mouse position in pixels."""

Interpreted = NewType("Interpreted", float)
"""Float in SliderValues domain."""

Controlled = NewType("Controlled", Any)
"""Value compatibile with handled controller."""
