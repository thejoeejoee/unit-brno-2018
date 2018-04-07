import numpy as np

from scipy.signal import medfilt2d


def erosion_filter(img: np.ndarray, level: int=5):
    """
    Removes smaller objects then specified size by level argument.
    """
    img = np.array(img, np.uint8)
    return medfilt2d(img, level)
