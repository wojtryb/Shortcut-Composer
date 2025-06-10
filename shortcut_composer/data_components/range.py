# SPDX-FileCopyrightText: © 2022-2025 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass
class Range:
    """
    Specifies contiguous range from `min` to `max` including both ends.

    `float("inf")` and `float("-inf")` can be used for infinite ranges.

    By default, the value change is linear, but it can be changed to
    exponential by providing exponent different than 1.

    ### Usage Examples:

    ```python
    Range(0, 100)          # All values from 0 to 100
    Range(0, float("inf")) # All values from 0 to infinity
    Range(0, 100, 3)       # Output changes exponentially with x^3
    ```
    """
    min: float
    max: float
    exponent: float = 1
