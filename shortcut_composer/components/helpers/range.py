from dataclasses import dataclass


@dataclass
class Range:
    """
    Specifies contiguous range from `min` to `max` including both ends.

    `float("inf")` and `float("-inf")` can be used for infinite ranges.
    """
    min: float
    max: float
