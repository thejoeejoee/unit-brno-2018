# coding=utf-8
from collections import defaultdict
from math import pi
from typing import DefaultDict

import numpy as np
from matplotlib import pyplot as plt

from unit.filters.edge_detection import high_pass
from unit.filters.erosion import erosion_filter


class HoughCircleDetector(object):
    GRADIENT_THRESHOLD = 40
    RADIUS_RANGE = (50, 100)

    def __init__(
            self,
            image,
            grads: np.ndarray,
            scale=10,
            vote_threshold=5
    ):
        self._scale = scale
        self._image = image
        self._grads = grads[::scale, ::scale]
        self._vote_threshold = vote_threshold

    def detect(self):
        shape = self._grads.shape
        radius_shape_count = abs(self.RADIUS_RANGE[0] - self.RADIUS_RANGE[1])
        H = np.zeros((radius_shape_count, shape[0], shape[1]))

        max_x, max_y = self._grads.shape[:2]
        t = np.linspace(0, 2 * pi, 20)
        coss = np.cos(t)
        sins = np.sin(t)

        over = defaultdict(set)  # type: DefaultDict[set]

        def gen_radius_f(rad):
            def bucketer(x, y):
                x, y = int(x), int(y)
                if self._grads[x, y] < self.GRADIENT_THRESHOLD:
                    return False

                def baf(row):
                    aa = row[0]
                    bb = row[1]
                    if 0 <= aa < max_y and 0 <= bb < max_x:
                        H[rad, int(aa), int(bb)] += 1
                        if H[rad, int(aa), int(bb)] > self._vote_threshold:
                            over[rad].add((aa, bb))

                a = x - coss * rad
                b = y - sins * rad
                np.apply_along_axis(baf, 1, np.dstack((a, b))[0])
                return True

            return bucketer

        for rad in range(self.RADIUS_RANGE[0] // self._scale, self.RADIUS_RANGE[1] // self._scale):
            np.fromfunction(
                np.vectorize(gen_radius_f(rad)),
                shape=shape
            )

        """
        fig = plt.figure()
        ax = Axes3D(fig)

        yxis, zaxis, xaxis = H.nonzero()

        ax.scatter(
            xaxis,
            yxis,
            zaxis
        )
        fig.show()
        input()
        """
        print(over)
        plt.imshow(erosion_filter(H[6, :, :], 3))
        plt.show()
        return

        def show_shape(patch):
            ax = plt.gca()
            ax.add_patch(patch)

        plt.imshow(self._image)
        for rad, circles in over.items():
            for x, y in circles:
                show_shape(plt.Circle((y * self._scale, x * self._scale), rad * self._scale, fc='none', ec='red'))

        plt.axis('scaled')

        plt.show()
