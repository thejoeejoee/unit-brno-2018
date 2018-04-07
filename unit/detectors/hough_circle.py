# coding=utf-8
from collections import defaultdict, namedtuple
from math import pi
from typing import DefaultDict, Dict

import numpy as np
from matplotlib import pyplot as plt

Circle = namedtuple('Circle', 'x y radius')


def show_shape(patch):
    ax = plt.gca()
    ax.add_patch(patch)


class HoughCircleDetector(object):
    GRADIENT_THRESHOLD = 40
    RADIUS_RANGE = (10, 120)

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
        t = np.linspace(0, 2 * pi, self._vote_threshold * 3)
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

        self._filter_centers(over, self._grads)

        return
        plt.imshow(self._image)
        for rad, circles in over.items():
            for x, y in circles:
                show_shape(plt.Circle((y, x), rad, fc='none', ec='red'))

        plt.axis('scaled')

        plt.show()

    def _filter_centers(self, over: Dict[int, set], grads: np.ndarray):
        side = self._grads.shape[0]

        entities = set()
        main_components = set()
        radius_count = len(over)

        for radius in sorted(over, reverse=True)[:int(radius_count // 1.5)]:
            to_process = list(over.get(radius))

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(int(x), int(y), int(radius))

                CIRCLE_THRESHOLD_RATIO = 0.1

                if any(self.is_too_near(candidate_circle, c, CIRCLE_THRESHOLD_RATIO) for c in main_components):
                    continue

                main_components.add(candidate_circle)

        main_components = {Circle(c.x, c.y, c.radius * 1.2) for c in main_components}
        groups = defaultdict(set)

        for radius in sorted(over, reverse=False)[:radius_count // 2]:
            to_process = list(over.get(radius))

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(int(x), int(y), int(radius))

                if any(self.is_too_near(candidate_circle, c, -.65) for c in entities):
                    continue
                for main in main_components:
                    if self.is_inside(
                            main=main,
                            to_check=candidate_circle
                    ):
                        groups[main].add(candidate_circle)
                        continue

        plt.imshow(self._image)

        color = iter(plt.cm.rainbow(np.linspace(0, 1, len(groups) * 2)))

        for main, entities in groups.items():  # type: Circle
            c = next(color)

            show_shape(
                plt.Circle(
                    (
                        main.y,
                        main.x  # + side // self._scale
                    ),
                    main.radius,
                    fc='none',
                    ec=c,
                    linestyle=':'
                )
            )

            for entity in entities:
                show_shape(
                    plt.Circle(
                        (
                            entity.y,
                            entity.x  # + side // self._scale
                        ),
                        entity.radius,
                        fc='none',
                        ec=c
                    )
                )

        plt.axis('scaled')
        plt.show()

        plt.imshow(self._image)

        for main1 in tuple(groups.keys()):
            for main2 in tuple(groups.keys()):
                if main1 != main2 and \
                        self.is_too_near(main1, main2, 0) \
                        and main2 in groups and main1 in groups \
                        and self.can_join_components(
                    main1, main2
                ):
                    new_main = Circle(
                        (main1.x + main2.x) / 2,
                        (main1.y + main2.y) / 2,
                        self.distance(main1, main2)
                    )
                    groups[new_main] = groups[main1] | groups[main2]
                    del groups[main2]
                    del groups[main1]

        for main, entities in groups.items():  # type: Circle
            c = next(color)

            show_shape(
                plt.Circle(
                    (
                        main.y,
                        main.x  # + side // self._scale
                    ),
                    main.radius,
                    fc='none',
                    ec=c,
                    linestyle=':'
                )
            )

            for entity in entities:
                show_shape(
                    plt.Circle(
                        (
                            entity.y,
                            entity.x  # + side // self._scale
                        ),
                        entity.radius,
                        fc='none',
                        ec=c
                    )
                )

        plt.axis('scaled')
        plt.show()

    def distance(self, c1, c2):
        return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** .5

    def is_inside(self, main: Circle, to_check: Circle):
        return (((main.x - to_check.x) ** 2 + (main.y - to_check.y) ** 2) ** .5) < main.radius

    def is_too_near(self, c1: Circle, c2: Circle, ratio: float) -> bool:
        dist = self.distance(c1, c2)
        R = c1.radius + c2.radius
        return (dist - R) < ratio * R

    def can_join_components(self, c1: Circle, c2: Circle):
        k = (c2.y - c1.y) / (c2.x - c1.x)
        q = c1.y - k * c1.x

        if c1.x < c2.x:
            x1 = c1.x
            x2 = c2.x
        else:
            x1 = c2.x
            x2 = c1.x

        if c1.y < c2.y:
            y1 = c1.y
            y2 = c2.y
        else:
            y1 = c2.y
            y2 = c1.y

        for x in range(int(x1), int(x2) + 1):
            y = int(round(k * x + q))
            if self._image[x, y] < self.GRADIENT_THRESHOLD:
                return False

        for y in range(int(y1), int(y2) + 1):
            x = int(round((y - q) / k))
            if self._image[x, y] < self.GRADIENT_THRESHOLD:
                return False

        return True
