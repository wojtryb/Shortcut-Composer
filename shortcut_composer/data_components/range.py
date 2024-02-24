# SPDX-FileCopyrightText: © 2022-2024 Wojciech Trybus <wojtryb@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass
class Range:
    """
    Specifies contiguous range from `min` to `max` including both ends.

    `float("inf")` and `float("-inf")` can be used for infinite ranges.

    ### Usage Examples:

    ```python
    Range(0, 100)          # All values from 0 to 100
    Range(0, float("inf")) # All values from 0 to infinity
    ```
    """
    min: float
    max: float
