# coding=utf-8

import csv

from unit.exporters.base import BaseExporter


class CsvExporter(BaseExporter):
    """
    Exports particles as CSV format into given fileobj.
    """
    HEADER_FIELD_NAMES = ['Width', 'Height', 'Max Length', 'Thickness']

    def export(self):
        writer = csv.writer(
            self._file_obj,
            dialect='excel',
        )

        writer.writerow(self.HEADER_FIELD_NAMES)
        writer.writerows(
            (p.width, p.height, p.max_length, p.thickness)
            for p
            in self._particles
            if p.width and p.thickness and p.height and p.max_length
        )
