from typing import NewType


MouseInput = NewType("MouseInput", int)
"""Integer returned by krita with a mouse position in pixels."""

Interpreted = NewType("Interpreted", float)
"""Float in SliderValues domain."""
