# coding=utf-8
from typing import Iterable, Type

from unit.exporters.base import BaseExporter
from unit.exporters.csv import CsvExporter
from unit.loader import Loader
from unit.particle import Particle


class Processor(object):
    def __init__(
            self,
            image_paths: Iterable[str],
            output_paths: Iterable[str],
            exporter_class: Type[BaseExporter] = CsvExporter
    ):
        self._loader = Loader(image_paths)
        self._image_paths = image_paths
        self._output_path = output_paths
        self._exporter_class = exporter_class

    def run(self):
        for path, image in zip(self._image_paths, self._loader.load_images()):
            print(path, image.shape)
            # TODO:

        # TODO:
        with open('out.csv', mode='w') as v:
            exporter = self._exporter_class((
                Particle(50, 30, 20, 15.5),
                Particle(85, 62, 30, 1 / 3.),
                Particle(20, 10, 30, 20),
            ), v)
            exporter.export()
