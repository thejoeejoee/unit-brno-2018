# coding=utf-8

import numpy as np


def threshold_image(image: np.ndarray, threshold: int) -> np.ndarray:
    """
    Filters image by threshold given by parameter.
    """

    return np.vectorize(lambda x: 255 if x > threshold else 0)(image)
