# coding=utf-8
from collections import defaultdict
from math import pi
from typing import DefaultDict, Dict

import numpy as np
from matplotlib import pyplot as plt
from sympy import Circle, Point, intersection


class HoughCircleDetector(object):
    GRADIENT_THRESHOLD = 40
    RADIUS_RANGE = (60, 100)

    def __init__(
            self,
            image,
            grads: np.ndarray,
            scale=10,
            vote_threshold=5
    ):
        self._scale = scale
        self._image = image[::scale, ::scale]
        self._grads = grads[::scale, ::scale]
        self._radius_range = self.RADIUS_RANGE[0] // scale, self.RADIUS_RANGE[1] // scale
        self._vote_threshold = vote_threshold

    def detect(self):
        shape = self._grads.shape
        radius_shape_count = abs(self._radius_range[0] + self._radius_range[1])
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
                    aa = int(row[0])
                    bb = int(row[1])
                    if 0 <= aa < max_y and 0 <= bb < max_x:
                        print(self._image[aa, bb])
                        if not self._image[aa, bb]:
                            return
                        H[rad, int(aa), int(bb)] += 1

                        if H[rad, int(aa), int(bb)] > self._vote_threshold:
                            over[rad].add((aa, bb))

                    try:
                        H[rad, int(aa) + 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        H[rad, int(aa) - 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        H[rad, int(aa), int(bb) + 1] += .25
                    except IndexError:
                        pass
                    try:
                        H[rad, int(aa), int(bb) - 1] += .25
                    except IndexError:
                        pass

                a = x - coss * rad
                b = y - sins * rad
                np.apply_along_axis(baf, 1, np.dstack((a, b))[0])
                return True

            return bucketer

        for rad in range(self._radius_range[0], self._radius_range[1]):
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

        # plt.imshow(H[6, :, :])
        # plt.show()

        # self._filter_centers(over, self._grads)

        # return

        def show_shape(patch):
            ax = plt.gca()
            ax.add_patch(patch)

        plt.imshow(self._image)
        for rad, circles in over.items():
            for x, y in circles:
                show_shape(plt.Circle((y, x), rad, fc='none', ec='red'))

        plt.axis('scaled')

        plt.show()

    def _filter_centers(self, over: Dict[int, set], grads: np.ndarray):
        side = self._grads.shape[0]

        entities = set()

        for radius in sorted(over, reverse=True):
            to_process = over.get(radius)

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(Point(int(x), int(y)), int(radius))

                if any(o.encloses(candidate_circle) for o in entities):
                    continue

                for maybe_collision in entities:
                    if intersection(candidate_circle, maybe_collision):
                        break
                else:
                    entities.add(candidate_circle)

        def show_shape(patch):
            ax = plt.gca()
            ax.add_patch(patch)

        plt.imshow(self._image)
        for entity in entities:  # type: Circle
            show_shape(
                plt.Circle(
                    (
                        side // self._scale - entity.center.x,
                        side // self._scale - entity.center.y  # + side // self._scale
                    ),
                    entity.radius,
                    fc='none', ec='red')
            )

        plt.axis('scaled')
        plt.show()
