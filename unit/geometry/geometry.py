# coding=utf-8
from typing import Tuple

import numpy as np


def bbox2(img: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Returns tight bounding box around object in img.
    """
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    r_min, r_max = np.where(rows)[0][[0, -1]]
    c_min, c_max = np.where(cols)[0][[0, -1]]
    #       y     y min       x     xmax
    return r_min, r_max, c_min, c_max


def longest_line(source: np.ndarray) -> int:
    """
    Finds longest line, nevermind on placement.
    """
    ymin, ymax, xmin, xmax = bbox2(source)
    source = source[ymin:ymax + 1][xmin:xmax + 1]
    max_len = 0

    for row in source:
        l = np.argwhere(row > 127)
        if l.size >= 2:
            max_len = max(max_len, l[-1] - l[0])
    return max_len


def longest_inline(source: np.ndarray):
    """
    Finds longest line placed IN object.
    """
    y_min, y_max, x_min, x_max = bbox2(source)
    source = source[y_min:y_max + 1][x_min:x_max + 1]
    max_len = 0

    for row in source:
        current_len = 0
        for value in row:
            if value >= 127:
                current_len += 1
            else:
                max_len = max(max_len, current_len)
                current_len = 0

    return max_len
