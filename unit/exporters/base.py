# coding=utf-8


from typing import Iterable, TextIO

from ..particle import Particle


class BaseExporter(object):
    """
    BaseExporter for results of detected particles.
    """

    def __init__(self, particles: Iterable[Particle], _file_obj: TextIO):
        self._particles = particles
        self._file_obj = _file_obj

    def export(self):
        raise NotImplementedError()
