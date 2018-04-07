# coding=utf-8
from argparse import ArgumentParser
from sys import argv

from unit.debug.comparator import ParticlesComparator


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('detected_csv', type=str, help='Path to CSV with detected.')
    parser.add_argument('origin_csv', type=str, help='Path to CSV with origin.')

    return parser


if __name__ == '__main__':
    parser_ = create_arg_parser()

    args = parser_.parse_args(argv[1:])

    ParticlesComparator.compare(
        open(args.detected_csv),
        open(args.origin_csv)
    )
