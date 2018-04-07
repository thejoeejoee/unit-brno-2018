# coding=utf-8
import logging
from collections import defaultdict, namedtuple
from math import pi
from typing import DefaultDict, Dict, Iterable, Tuple, Set, Callable

import numpy as np
from matplotlib import pyplot as plt

Circle = namedtuple('Circle', 'x y radius')


class HoughCircleDetector(object):
    """
    With Hough's circle transform tries to detect main circled component on image.
    For each of bigger components are computed "stats" about radius probability.
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
        return self._scale

    def detect(self) -> Iterable[Tuple[int, int, int, int]]:
        """
        From loaded image detect all AABB boxes around particles.
        """
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
            accumulator=accumulator,
            over=over,
            coss=np.cos(t),
            sins=np.sin(t),
        )
        for rad in range(self._radius_range[0], self._radius_range[1]):
            # accumulate all needed radiuses
            logging.debug('Computing radius stats on level {}...'.format(rad))
            np.fromfunction(
                np.vectorize(gen_radius_f(rad)),
                shape=shape
            )

        groups = self._create_groups(over, self._grads)
        return self._generate_boxes(groups)

    def _create_groups(self, over: Dict[int, set], grads: np.ndarray) -> Dict[Circle, Set[Circle]]:
        """
        From rated radiuses creates main components with their main subcomponents,
        using clustering and analytic geometry.
        """
        entities = set()
        radius_count = len(over)
        logging.debug('Removing components on sides.')
        over = {
            radius: tuple(self._remove_image_edges_components(radius, circles)) for radius, circles in over.items()
        }

        main_components = self._place_main_components(over, radius_count)
        logging.debug('Placed {} main components.'.format(len(main_components)))
        main_components = {Circle(int(c.x), int(c.y), int(c.radius * 1.2)) for c in main_components}

        groups = self._place_minor_components(entities, main_components, over, radius_count)
        logging.debug('Minor components placed into {} groups.'.format(len(groups)))
        # color = iter(plt.cm.rainbow(np.linspace(0, 1, 100)))

        # plt.imshow(self._image.T)

        # self._debug_plot_components(color, groups)

        self._join_near_main_components(groups)
        logging.debug('Groups joined total to {}.'.format(len(groups)))

        # self._debug_plot_components(color, groups)

        # self._debug_plot_boxes(self._generate_boxes(groups))

        # plt.show()

        return groups

    def _generate_cone_radius_callable(self, max_x: int, max_y: int, accumulator: np.ndarray, over: Dict,
                                       coss: np.ndarray, sins: np.ndarray) -> Callable:
        """
        Create callable for walking though bevel gradients arrays and accumulating them into array.
        """

        def gen_radius_f(rad: int) -> Callable:
            def bucketer(x: int, y: int):
                x, y = int(x), int(y)
                if self._grads[x, y] < self.GRADIENT_THRESHOLD:
                    return False

                def accumulate(row):
                    aa = int(row[0])
                    bb = int(row[1])
                    if 0 <= aa < max_y and 0 <= bb < max_x:
                        if not self._image[aa, bb]:
                            return
                        accumulator[rad, int(aa), int(bb)] += 1

                        if accumulator[rad, int(aa), int(bb)] > self._vote_threshold:
                            over[rad].add((aa, bb))

                    try:
                        accumulator[rad, int(aa) + 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        accumulator[rad, int(aa) - 1, int(bb)] += .25
                    except IndexError:
                        pass
                    try:
                        accumulator[rad, int(aa), int(bb) + 1] += .25
                    except IndexError:
                        pass
                    try:
                        accumulator[rad, int(aa), int(bb) - 1] += .25
                    except IndexError:
                        pass

                a = x - coss * rad
                b = y - sins * rad
                np.apply_along_axis(accumulate, 1, np.dstack((a, b))[0])
                return True

            return bucketer

        return gen_radius_f

    def _join_near_main_components(self, groups: Dict[Circle, Set[Circle]]):
        """
        Tries to join all near main components - based od distance and collisions.
        New created are added to groups and recurently added to possibility joins.
        """
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
        """
        Tries place minor component into major (main) components - decision based on enclosing and distance.
        """
        groups = defaultdict(set)
        for radius in sorted(over, reverse=False)[:radius_count // 2]:
            to_process = list(over.get(radius))

            while to_process:
                x, y = to_process.pop()
                candidate_circle = Circle(int(x), int(y), int(radius))

                if any(self.is_too_near(candidate_circle, c, ratio=-.75) for c in entities):
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
        """
        Tries to place main components into image - decisions based on distance between others.
        """
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
        """
        Removes all components with sides outside image shape.
        """
        max_x = self._image.shape[0]
        max_y = self._image.shape[1]
        for x, y in circles:
            if min((x, y, max_x - x, max_y - y)) > radius * ratio:
                yield (x, y)

    def _generate_boxes(self, groups: Dict[Circle, Set[Circle]], ratio=0.015):
        """
        From groups of main components generates boxes from their minimal/maximal X/Y.
        """
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
            if not (max_y > min_y) or not (max_x > min_x):
                continue

            yield (
                min_x - side * (ratio / 2),
                min_y - side * (ratio / 2),
                (max_x - min_x) + side * ratio,
                (max_y - min_y) + side * ratio
            )

    def _can_join_components(self, c1: Circle, c2: Circle):
        """
        Detects, if two components can be joined - exists active full path on image between centers.
        """
        u1 = (c2.x - c1.x)
        u2 = (c2.y - c1.y)
        a1 = c1.x
        a2 = c1.y
        side = self._image.shape[0]

        r = int(min(c1.radius, c2.radius) * 1)
        for rat in (.25, .5, .75, .1,):
            for t in np.linspace(0, 1, 30):
                x1 = int(round(a1 + t * u1))
                y1 = int(round(a2 + t * u2))
                x2 = int(round(a1 + r * rat + t * u1))
                y2 = int(round(a2 + r * rat + t * u2))
                x3 = int(round(a1 - r * rat + t * u1))
                y3 = int(round(a2 - r * rat + t * u2))

                twices = (x1, y1), (x2, y2), (x3, y3)

                def is_ok(x, y):
                    return 0 <= x < side and 0 <= y < side

                if all((self._image[tw] < self.GRADIENT_THRESHOLD) for tw in twices if is_ok(*tw)):
                    return False

        return True

    @staticmethod
    def distance(c1, c2):
        """Returns distance between centers two circles."""
        return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** .5

    @staticmethod
    def is_inside(main: Circle, to_check: Circle):
        """Returns, if to_check Circle is inside of main Circle."""
        return (((main.x - to_check.x) ** 2 + (main.y - to_check.y) ** 2) ** .5) < main.radius

    @classmethod
    def is_too_near(cls, c1: Circle, c2: Circle, ratio: float) -> bool:
        """Returns, if two circles has overlap higher then ration of sum of their radiuses."""
        dist = cls.distance(c1, c2)
        R = c1.radius + c2.radius
        return (dist - R) < ratio * R

    def _debug_plot_circles(self, over):
        plt.imshow(self._image)
        for rad, circles in over.items():
            for x, y in circles:
                self._debug_show_shape(plt.Circle((y, x), rad, fc='none', ec='red'))
        plt.axis('scaled')
        plt.show()

    def _debug_plot_boxes(self, boxes):
        for x, y, w, h in boxes:
            self._debug_show_shape(
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

            self._debug_show_shape(
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
                self._debug_show_shape(
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

    @staticmethod
    def _debug_show_shape(patch):
        ax = plt.gca()
        ax.add_patch(patch)
