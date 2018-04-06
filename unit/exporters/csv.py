# coding=utf-8

import csv

from unit.exporters.base import BaseExporter
from unit.particle import Particle


class CsvExporter(BaseExporter):
    """
    Exports particles as CSV format into given fileobj.
    """

    def export(self):
        writer = csv.writer(
            self._file_obj,
            dialect='excel',
        )

        writer.writerow(Particle.HEADER_FIELD_NAMES)
        writer.writerows(
            (i, p.width, p.height, p.max_length, p.thickness)
            for i, p
            in enumerate(self._particles, start=1)
            if p.width and p.thickness and p.height and p.max_length
        )
