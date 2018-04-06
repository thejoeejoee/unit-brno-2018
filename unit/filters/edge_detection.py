# coding=utf-8
import numpy as np
from math import pi
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


def sony(source: np.ndarray):
    print(source)
    averaged = generic_filter(source, np.matrix([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]]
    ))

    def normalize(x):
        if x == 255 * 8:
            return 0
        elif x == 0:
            return 0
        else:
            return 255

    vfunc = np.vectorize(normalize)
    return vfunc(averaged)

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
    #thetas = np.vectorize(normalize_angle)(thetas)

    grads = np.hypot(grad_y, grad_x)
    return grads, thetas


def high_pass(source: np.ndarray, a=1):
    return generic_filter(source, np.matrix([
        [-a, -a, -a],
        [-a, 9 + 8 * a, -a],
        [-a, -a, -a],
    ])) * (1. / 9)
