# coding=utf-8
from typing import Tuple

import numpy as np
from scipy.signal import convolve2d


def generic_filter(source: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """
    Generic version for 2D convolve filtration specified by filter matrix.
    """
    return convolve2d(source, matrix)


def gaussian_filter(source: np.ndarray) -> np.ndarray:
    """
    Applies Gaussian filter with 5*5 matrix.
    """
    return generic_filter(source, np.matrix([
        [2, 4, 5, 4, 2],
        [4, 9, 12, 9, 4],
        [5, 12, 15, 12, 5],
        [4, 9, 12, 9, 4],
        [2, 4, 5, 4, 2],
    ])) * (1. / 159)


def sobel_gradients(source: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes partial derivations to detect angle gradients.
    """
    grad_x = generic_filter(source, np.matrix([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1]]
    ))

    grad_y = generic_filter(source, np.matrix([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]]
    ))

    def normalize_angle(x: float) -> int:
        x = round(x % 180)
        if x >= 0 and x <= 22.5:
            return 0
        elif x > 22.5 and x <= 67.5:
            return 45
        elif x > 67.5 and x <= 112.5:
            return 90
        elif x > 112.5 and x <= 157.5:
            return 135
        elif x > 157.5 and x <= 180:
            return 0

    thetas = np.arctan2(grad_y, grad_x)
    thetas = np.vectorize(normalize_angle)(thetas)

    grads = np.hypot(grad_y, grad_x)
    return grads, thetas


def high_pass(source: np.ndarray, a=1):
    """
    High pass filters for 2D with alpha value.
    """
    return generic_filter(source, np.matrix([
        [-a, -a, -a],
        [-a, 9 + 8 * a, -a],
        [-a, -a, -a],
    ])) * (1. / 9)
