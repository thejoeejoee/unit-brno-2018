# coding=utf-8
from collections import defaultdict, namedtuple
from math import pi
from typing import DefaultDict, Dict, Iterable, Tuple, Set

import numpy as np
from matplotlib import pyplot as plt

Circle = namedtuple('Circle', 'x y radius')


def show_shape(patch):
    ax = plt.gca()
    ax.add_patch(patch)


class HoughCircleDetector(object):
    """
    With Hough's circle transform tries to detect main circled component on image.
    """
    GRADIENT_THRESHOLD = 40
    RADIUS_RANGE = (10, 120)

    def __init__(
            self,
            image: np.ndarray,
            grads: np.ndarray,
            scale: int = 10,
            vote_threshold: int = 4
    ):
        self._scale = scale
        self._image = image[::scale, ::scale]
        self._grads = grads[::scale, ::scale]
        self._radius_range = self.RADIUS_RANGE[0] // scale, self.RADIUS_RANGE[1] // scale
        self._vote_threshold = vote_threshold

    @property
    def scale(self) -> int:
        return self.scale

    def detect(self):
        shape = self._grads.shape
        radius_shape_count = abs(self._radius_range[0] + self._radius_range[1])  # type: int
        # accumulator array
        accumulator = np.zeros((radius_shape_count, shape[0], shape[1]))  # type: np.ndarray

        max_x, max_y = self._grads.shape[:2]
        # linspace for goniometric functions
        t = np.linspace(0, 2 * pi, self._vote_threshold * 3)

        over = defaultdict(set)  # type: DefaultDict[Circle, set]

        gen_radius_f = self._generate_cone_radius_callable(
            max_x=max_x,
            max_y=max_y,
            acumulator=accumulator,
            over=over,
            coss=np.cos(t),
            sins=np.sin(t),
        )

        for rad in range(self._radius_range[0], self._radius_range[1]):
            # accumulate all needed radiuses
            np.fromfunction(
                np.vectorize(gen_radius_f(rad)),
                shape=shape
            )
        groups = self._create_groups(over, self._grads)
        return self._generate_boxes(groups)

    def _create_groups(self, over: Dict[int, set], grads: np.ndarray) -> Dict[Circle, Set[Circle]]:
        entities = set()
        radius_count = len(over)

        over = {
            radius: tuple(self._remove_image_edges_components(radius, circles)) for radius, circles in over.items()
        }

        main_components = self._place_main_components(over, radius_count)

        main_components = {Circle(int(c.x), int(c.y), int(c.radius * 1.2)) for c in main_components}

        groups = self._place_minor_components(entities, main_components, over, radius_count)

        color = iter(plt.cm.rainbow(np.linspace(0, 1, 100)))

        plt.imshow(self._image.T)

        # self._debug_plot_components(color, groups)

        # plt.show()

        self._join_near_main_components(groups)

        # self._debug_plot_components(color, groups)

        #self._debug_plot_boxes(self._generate_boxes(groups))

        return groups

    def _generate_cone_radius_callable(self, max_x, max_y, acumulator, over, coss, sins):
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
                        acumulator[rad, int(aa), int(bb)] += 1

                        if acumulator[rad, int(aa), int(bb)] > self._vote_threshold:
                            over[rad].add((aa, bb))

                    try:
                        acumulator[rad, int(aa) + 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        acumulator[rad, int(aa) - 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        acumulator[rad, int(aa), int(bb) + 1] += .25
                    except IndexError:
                        pass
                    try:
                        acumulator[rad, int(aa), int(bb) - 1] += .25
                    except IndexError:
                        pass

                a = x - coss * rad
                b = y - sins * rad
                np.apply_along_axis(baf, 1, np.dstack((a, b))[0])
                return True

            return bucketer

        return gen_radius_f

    def _join_near_main_components(self, groups):
        to_process = set(groups.keys())

        while to_process:
            candidate = to_process.pop()

            for another in tuple(to_process):
                if candidate != another and self.is_too_near(candidate, another, 12) and self._can_join_components(
                        candidate, another
                ):
                    new_main = Circle(
                        (another.x + candidate.x) / 2,
                        (another.y + candidate.y) / 2,
                        self.distance(another, candidate)
                    )
                    if candidate in groups:
                        del groups[candidate]
                    if another in groups:
                        del groups[another]

                    groups[new_main] = groups[another] | groups[candidate]
                    to_process.add(new_main)
                    break
            else:
                break

    def _place_minor_components(self, entities, main_components, over, radius_count):
        groups = defaultdict(set)
        for radius in sorted(over, reverse=False)[:radius_count // 2]:
            to_process = list(over.get(radius))

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(int(x), int(y), int(radius))

                if any(self.is_too_near(candidate_circle, c, ratio=-.65) for c in entities):
                    continue
                for main in main_components:
                    if self.is_inside(
                            main=main,
                            to_check=candidate_circle
                    ) and self._can_join_components(
                        c1=main,
                        c2=candidate_circle
                    ):
                        groups[main].add(candidate_circle)
                        continue
        return groups

    def _place_main_components(self, over, radius_count):
        main_components = set()
        for radius in sorted(over, reverse=True)[:int(radius_count // 1.25)]:
            to_process = list(over.get(radius))

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(int(x), int(y), int(radius))

                if any(self.is_too_near(candidate_circle, c, ratio=0.1) for c in main_components):
                    continue

                main_components.add(candidate_circle)
        return main_components

    def _remove_image_edges_components(self, radius: int, circles: Iterable[Tuple[int, int]], ratio=1.35):
        max_x = self._image.shape[0]
        max_y = self._image.shape[1]
        for x, y in circles:
            if min((x, y, max_x - x, max_y - y)) > radius * ratio:
                yield (x, y)

    def _can_join_components_(self, c1: Circle, c2: Circle):
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

    def _generate_boxes(self, groups: Dict[Circle, Set[Circle]], ratio=0.015):
        side = self._image.shape[0]
        for main, components in groups.items():
            min_x = side
            min_y = side
            max_x = 0
            max_y = 0
            for c in components:
                max_x = max((max_x, c.x + c.radius))
                min_x = min((min_x, c.x - c.radius))
                max_y = max((max_y, c.y + c.radius))
                min_y = min((min_y, c.y - c.radius))

            yield (
                min_x - side * (ratio / 2),
                min_y - side * (ratio / 2),
                (max_x - min_x) + side * ratio,
                (max_y - min_y) + side * ratio
            )

    def _can_join_components(self, c1: Circle, c2: Circle):
        u1 = (c2.x - c1.x)
        u2 = (c2.y - c1.y)
        a1 = c1.x
        a2 = c1.y

        r = int(min(c1.radius, c2.radius) * 1)
        for rat in (.25, .5, .75, .1,):
            for t in np.linspace(0, 1, 30):
                x1 = int(round(a1 + t * u1))
                y1 = int(round(a2 + t * u2))
                x2 = int(round(a1 + r * rat + t * u1))
                y2 = int(round(a2 + r * rat + t * u2))
                x3 = int(round(a1 - r * rat + t * u1))
                y3 = int(round(a2 - r * rat + t * u2))
                if all((
                        self._image[x1, y1] < self.GRADIENT_THRESHOLD,
                        self._image[x2, y2] < self.GRADIENT_THRESHOLD,
                        self._image[x3, y3] < self.GRADIENT_THRESHOLD,
                )):
                    return False

        return True

    @staticmethod
    def distance(c1, c2):
        return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** .5

    @staticmethod
    def is_inside(main: Circle, to_check: Circle):
        return (((main.x - to_check.x) ** 2 + (main.y - to_check.y) ** 2) ** .5) < main.radius

    @classmethod
    def is_too_near(cls, c1: Circle, c2: Circle, ratio: float) -> bool:
        dist = cls.distance(c1, c2)
        R = c1.radius + c2.radius
        return (dist - R) < ratio * R

    def _debug_plot_circles(self, over):
        plt.imshow(self._image)
        for rad, circles in over.items():
            for x, y in circles:
                show_shape(plt.Circle((y, x), rad, fc='none', ec='red'))
        plt.axis('scaled')
        plt.show()

    def _debug_plot_boxes(self, boxes):
        for x, y, w, h in boxes:
            show_shape(
                plt.Rectangle(
                    (x, y),
                    w,
                    h,
                    fc='none',
                    ec='red',
                    lw=2,
                    linestyle='--'
                )
            )
        plt.axis('scaled')
        plt.show()

    def _debug_plot_components(self, color, groups):
        for main, entities in groups.items():  # type: Circle

            c = next(color)

            show_shape(
                plt.Circle(
                    (
                        main.x,
                        main.y  # + side // self._scale
                    ),
                    main.radius,
                    fc='none',
                    ec=c,
                    linestyle=':',
                    lw=4
                )
            )

            for entity in entities:
                show_shape(
                    plt.Circle(
                        (
                            entity.x,
                            entity.y  # + side // self._scale
                        ),
                        entity.radius,
                        fc='none',
                        ec=c
                    )
                )
