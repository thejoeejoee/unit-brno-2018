#!/usr/bin/env python3
# coding=utf-8
import sys
from argparse import ArgumentParser

from unit.processor import Processor


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.description = 'Command line application for detecting circled particles on TIFF image with CSV particle ' \
                         'export. '
    parser.add_argument('input_tiff_file', type=str, help='Path to tiff file to parse.')
    parser.add_argument('output_csv', type=str, help='Path to CSV file to generate, use - for stdout.')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debug mode to compare particles with origin.')

    return parser


def main() -> int:
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    processor = Processor()
    if not args.debug:
        with open(args.output_csv, 'w') as f:
            return processor.run(
                args.input_tiff_file,
                f,
            )


if __name__ == '__main__':
    exit(main())
