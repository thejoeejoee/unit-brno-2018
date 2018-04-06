# coding=utf-8
import os
from typing import Generator, Iterable

import numpy as np
from libtiff import TIFF

from unit.exceptions import TiffLoadError
from .exceptions import ImageNotFoundError


class Loader(object):
    def __init__(self, paths: Iterable[str]):
        self._paths = paths

    def load_images(self) -> Generator[np.ndarray, None, None]:
        for path_ in self._paths:
            if not os.path.exists(path=path_):
                raise ImageNotFoundError(path_)

            try:
                tiff = TIFF.open(filename=path_, mode='r')
            except IOError as e:
                raise TiffLoadError() from e

            yield from tiff.iter_images()
