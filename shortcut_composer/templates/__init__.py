# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Templates allowing to create actions using logic related to key events.

Available templates:
- `PieMenu`
- `CursorTracker`
- `MultipleAssignment`
- `TemporaryKey`
- `RotationSelector`
- `RawInstructions`

All templates must implement ComplexAction interface, so that they can be
used by the ShortcutAdapter.

Each template implements different logic based pressing and releasing of
the related keys.
"""

from .multiple_assignment import MultipleAssignment
from .rotation_selector import RotationSelector
from .raw_instructions import RawInstructions
from .cursor_tracker import CursorTracker
from .temporary_key import TemporaryKey
from .pie_menu import PieMenu


__all__ = [
    'MultipleAssignment',
    'RawInstructions',
    'CursorTracker',
    'RotationSelector',
    'TemporaryKey',
    'PieMenu']
