# coding=utf-8
from unit.loader import Loader


class Processor(object):
    def __init__(self, image_paths, output_paths):
        self._loader = Loader(image_paths)
        self._image_paths = image_paths
        self._output_path = output_paths

    def run(self):
        for path, image in zip(self._image_paths, self._loader.load_images()):
            print(path, image.shape)
            # TODO:
