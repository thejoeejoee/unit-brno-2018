# coding=utf-8
from typing import Type, TextIO, Iterable

import matplotlib.pyplot as plt
import numpy

from unit.exporters.base import BaseExporter
from unit.exporters.csv import CsvExporter
from unit.filters.edge_detection import gaussian_filter, sobel
from unit.filters.threshold import threshold_image
from unit.loader import Loader
from unit.particle import Particle


class Processor(object):
    def __init__(
            self,
            exporter_class: Type[BaseExporter] = CsvExporter,
            loader_class: Type[Loader] = Loader,
    ):
        self._exporter_class = exporter_class
        self._loader_class = loader_class

    def run(self, input_path: str, output_stream: TextIO):
        return self.multiple_run(
            inputs=(input_path,),
            outputs=(output_stream,),
        )

    def multiple_run(self, inputs: Iterable[str], outputs: Iterable[TextIO]) -> None:
        loader = self._loader_class(*inputs)

        for image, output_stream in zip(loader.load_images(), outputs):
            particles = self._detect_particles(image=image)
            exporter = self._exporter_class(particles=particles, _file_obj=output_stream)
            exporter.export()

    def _detect_particles(self, image: numpy.ndarray) -> Iterable[Particle]:
        # TODO: use filters and all magic around to resolve image particles

        fig = plt.figure(figsize=(4, 4))
        print(image.shape)

        fig.add_subplot(1, 2, 1)
        plt.imshow(image, cmap='gray')
        fig.add_subplot(1, 2, 2)

        image = threshold_image(image, 80)
        image = gaussian_filter(image)
        image, t = sobel(image)
        """image = threshold_image(generic_filter(image, np.matrix(
[[1, 0, -1],
[2, 0, -2],
[1, 0 , -1]])
               ), 30)"""
        plt.imshow(image, cmap='gray')
        plt.show()

        return []
