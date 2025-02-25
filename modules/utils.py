"""
(Helper Functions)
Contains utility functions that don’t belong in a specific class.
"""

import numpy as np


def calculate_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.

    Args:
        p1 (tuple): First point (x, y).
        p2 (tuple): Second point (x, y).

    Returns:
        float: Distance between the points.
    """
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
