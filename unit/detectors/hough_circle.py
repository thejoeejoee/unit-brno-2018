# coding=utf-8
from math import pi, cos, sin

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class HoughCircleDetector(object):
    def __init__(self, grads: np.ndarray, thetas: np.ndarray, radius_range=(10, 40)):
        self._grads = grads
        self._thetas = thetas
        self._radius_range = radius_range

    def detect(self):
        shape = self._grads.shape

        min_radius, max_radius = self._radius_range
        H = np.zeros((shape[0], shape[1]))# + (max_radius - min_radius,))

        max_x, max_y = self._grads.shape[:2]
        space = np.linspace(0, 2 * pi, 7)
        space_n = len(space)
        coss = [cos(r + pi) for r in space]
        sins = [sin(r + pi) for r in space]

        def gen_radius_f(rad):
            def bucketer(x, y):
                x, y = int(x), int(y)
                if self._grads[x, y] < 5:
                    return False

                for t in range(space_n):
                    # radians = self._thetas[x, y]
                    a = int(round(x - rad * coss[t]))
                    b = int(round(y - rad * sins[t]))
                    if 0 <= a < max_y and 0 <= b < max_x:
                        H[a][b] += 1

                return True

            return bucketer

        for rad in range(*self._radius_range):
            np.fromfunction(
                np.vectorize(gen_radius_f(rad)),
                shape=shape
            )

        # result = [[0 for i in range(max_x)] for _ in range(max_y)]
        # for y in range(max_x):
        #     for x in range(max_y):
        #         if self._grads[y][x] > 5:
        #             for t in np.linspace(0, 2 * pi, 360):
        #                 # t = theta[y][x]
        #                 radius = 40
        #                 a = round(x - radius * cos(t))
        #                 b = round(y - radius * sin(t))
        #                 if 0 <= a < max_y and 0 <= b < max_x:
        #                     result[a][b] += 1

        plt.imshow(H)
        plt.show()
        return

        fig = plt.figure()
        ax = Axes3D(fig)

        xaxis, yxis, zaxis = H.nonzero()

        ax.scatter(
            xaxis,
            yxis,
            zaxis
        )
        fig.show()
        input()
