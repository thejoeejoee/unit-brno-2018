# coding=utf-8
import csv
from itertools import islice, zip_longest
from typing import Iterable, TextIO

from ..particle import Particle


class ParticlesComparator(object):
    def __init__(self):
        pass

    def compare(
            self,
            detected_particles: Iterable[Particle],
            origin_particles_file: TextIO
    ):
        pass

        loader = csv.reader(origin_particles_file)
        loaded_particles = []
        for particle_row in islice(loader, 1, None):
            loaded_particles.append(Particle.from_row(particle_row))

        loaded_particles = sorted(
            ((particle.max_length * particle.thickness), particle) for particle in loaded_particles
        )

        detected_particles = sorted(
            ((particle.max_length * particle.thickness), particle) for particle in detected_particles
        )

        for first, second in zip_longest(
                loaded_particles,
                detected_particles,
                fillvalue=(0, None)
        ):
            size_a, a = first
            size_b, b = second
            print(
                '{:2f}\t{}\t{:.2f}\t{}'.format(
                    float(size_a),
                    str(a) or '',
                    float(size_b),
                    str(b) or '',
                )
            )
