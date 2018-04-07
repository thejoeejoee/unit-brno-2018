# coding=utf-8
import numpy as np

def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    #       y     y min       x     xmax
    return rmin, rmax, cmin, cmax

def get_longest_line(source):
    ymin, ymax, xmin, xmax = bbox2(source)
    source = source[ymin:ymax + 1][xmin:xmax + 1]
    max_len = 0
    for row in source:
        current_len = 0
        for value in row:
            if value == 255:
                current_len += 1
            else:
                max_len = max(max_len, current_len)
                current_len = 0
    return max_len

"""
maxi = 0
    for i in range(0, 180, 5):
        maxi = max(maxi, get_longest_line(ndimage.interpolation.rotate(img, i)))
    print("max", maxi)
    """