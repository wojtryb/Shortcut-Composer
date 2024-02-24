# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NewType


MouseInput = NewType("MouseInput", int)
"""Integer returned by krita with a mouse position in pixels."""

Interpreted = NewType("Interpreted", float)
"""Float in SliderValues domain."""
