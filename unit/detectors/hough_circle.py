# coding=utf-8
from math import pi, cos, sin

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class HoughCircleDetector(object):
    def __init__(self, grads: np.ndarray, thetas: np.ndarray, radius_range=(30 // 5, 50 // 5)):
        self._grads = grads[::5, ::5]
        self._thetas = thetas
        self._radius_range = radius_range

    def detect(self):
        shape = self._grads.shape

        min_radius, max_radius = self._radius_range
        H = np.zeros((shape[0], shape[1]))# + (max_radius - min_radius,))

        max_x, max_y = self._grads.shape[:2]
        t = np.linspace(0, 2 * pi, 20)
        coss = np.cos(t)
        sins = np.sin(t)

        def gen_radius_f(rad):
            def bucketer(x, y):
                x, y = int(x), int(y)
                if self._grads[x, y] < 40:
                    return False

                def baf(row):
                    aa = row[0]
                    bb = row[1]
                    if 0 <= aa < max_y and 0 <= bb < max_x:
                        H[int(aa)][int(bb)] += 1

                a = x - coss * rad
                b = y - sins * rad
                np.apply_along_axis(baf, 1, np.dstack((a, b))[0])
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
