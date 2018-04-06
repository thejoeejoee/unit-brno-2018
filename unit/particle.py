# coding=utf-8


class Particle(object):
    width = 0  # type: int
    height = 0  # type: int
    max_length = 0.0  # type: float
    thickness = 0.0  # type: float

    def __init__(self, width=0, height=0, max_length=0, thickness=0):
        self.width = width
        self.height = height
        self.max_length = max_length
        self.thickness = thickness
