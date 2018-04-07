# coding=utf-8
from typing import Iterable


class Particle(object):
    """
    Class representing one particle detected in image.
    """
    HEADER_FIELD_NAMES = ['Width', 'Height', 'Max Length', 'Thickness']
    width = 0  # type: int
    height = 0  # type: int
    max_length = 0.0  # type: float
    thickness = 0.0  # type: float

    def __init__(self, width=0, height=0, max_length=0, thickness=0):
        self.width = width
        self.height = height
        self.max_length = max_length
        self.thickness = thickness

    @classmethod
    def from_row(cls, row: Iterable[str]):
        if len(row) > len(cls.HEADER_FIELD_NAMES):
            row = row[1:]

        particle = cls()
        particle.width, particle.height, particle.max_length, particle.thickness = row

        particle.width = int(particle.width)
        particle.height = int(particle.height)
        particle.max_length = float(particle.max_length)
        particle.thickness = float(particle.thickness)

        return particle

    def __str__(self):
        return 'Particle({})'.format(
            ', '.join(
                '{}={:3}'.format(
                    k[0],
                    str(getattr(self, k, None))
                ) for k in sorted(dir(self)) if
                not k.startswith('_') and not k[0].isupper() and not callable(getattr(self, k, None))
            )
        )

    def __lt__(self, other):
        return self.width > other.width
