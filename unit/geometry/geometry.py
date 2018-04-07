# coding=utf-8
import numpy as np


def bbox2(img):
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    #       y     y min       x     xmax
    return rmin, rmax, cmin, cmax

def longest_line(source):
    ymin, ymax, xmin, xmax = bbox2(source)
    source = source[ymin:ymax + 1][xmin:xmax + 1]
    max_len = 0

    for row in source:
        l = np.argwhere(row > 127)
        if l.size >= 2:
            max_len = max(max_len, l[-1] - l[0])
    return max_len

def longest_inline(source):
    ymin, ymax, xmin, xmax = bbox2(source)
    source = source[ymin:ymax + 1][xmin:xmax + 1]
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

"""
maxi = 0
    maxi_angle = 0
    for i in range(0, 180, 1):
        line = get_longest_line(ndimage.interpolation.rotate(img, i))
        if maxi < line:
            maxi = line
            maxi_angle = i


    print(get_longest_inline(ndimage.interpolation.rotate(img, maxi_angle + 90)))
"""