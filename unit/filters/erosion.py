import numpy as np

from scipy.signal import medfilt2d


def erosion_filter(img, level=5):
    img = np.array(img, np.uint8)
    return medfilt2d(img, level)
