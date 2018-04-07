# coding=utf-8
import logging
import os
from typing import Generator

import numpy as np
from libtiff import TIFF

from unit.exceptions import TiffLoadError
from .exceptions import ImageNotFoundError


class Loader(object):
    """
    Class for loading TIFF images specified as paths.
    """

    def __init__(self, *paths: str):
        self._paths = paths

    def load_images(self) -> Generator[np.ndarray, None, None]:
        """
        Loads TIFF images from paths as numpy arrays.
        """
        for path_ in self._paths:
            if not os.path.exists(path=path_):
                raise ImageNotFoundError(path_)

            try:
                tiff = TIFF.open(filename=path_, mode='r')
            except IOError as e:
                raise TiffLoadError() from e

            for im in tiff.iter_images():
                arr = np.array(im, np.uint8)
                if len(arr.shape) > 2:
                    logging.warning(
                        'Image {} has not two dimensional greyscale data, '
                        'actually has shape of {} - filtering first dimension.'.format(
                            path_,
                            arr.shape
                        ))
                    yield arr[:, :, 0]

                yield arr
