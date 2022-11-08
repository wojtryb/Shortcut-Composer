"""
Templates allowing to create actions using logic related to key events.

Available templates:
- `TemporaryKey`
- `MultipleAssignment`
- `MouseTracker`

All templates must implement PluginAction interface, so that they can be
used by the ShortcutAdapter.

Each template implements different logic based pressing and releasing of
the related keys.
"""

from .multiple_assignment import MultipleAssignment
from .temporary_key import TemporaryKey
from .mouse_tracker import MouseTracker


__all__ = [
    'MultipleAssignment',
    'TemporaryKey',
    'MouseTracker',
]
