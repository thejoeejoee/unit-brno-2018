# coding=utf-8
import numpy as np
from scipy.signal import convolve2d


def generic_filter(source: np.ndarray, filter: np.ndarray) -> np.ndarray:
    return convolve2d(source, filter)


def gaussian_filter(source: np.ndarray) -> np.ndarray:
    return generic_filter(source, np.matrix([
        [2, 4, 5, 4, 2],
        [4, 9, 12, 9, 4],
        [5, 12, 15, 12, 5],
        [4, 9, 12, 9, 4],
        [2, 4, 5, 4, 2],
    ])) * (1. / 159)


def sobel(source: np.ndarray):
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

    grads = np.hypot(grad_x, grad_y)
    thetas = np.arctan2(grad_y, grad_x)
    return grads, thetas
