# coding=utf-8

import numpy as np



def threshold_image(image: np.ndarray, threshold: int) -> np.ndarray:
    thresholder = lambda x: 255 if x > threshold else 0
    vfunc = np.vectorize(thresholder)

    return vfunc(image)
