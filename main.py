#!/usr/bin/env python3
# coding=utf-8
import logging
import sys
from argparse import ArgumentParser

from unit.exceptions import ImageNotFoundError, TiffLoadError
from unit.processor import Processor


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Command line application for detecting circled particles on TIFF image with CSV particle " \
                    "export. ",
        epilog="""
            Authors: Josef Kolář, Son Hai Nguyen, Tina Heindlová, Jan Vykydal, MIT, 2018
        """
    )
    parser.add_argument('input_tiff_file', type=str, help='Path to tiff file to parse.')
    parser.add_argument('output_csv', type=str, help='Path to CSV file to generate, use - for stdout.')

    parser.add_argument('--verbose', action='store_true', default=False,
                        help='Enable debug mode enable verbose output.')

    return parser


def main() -> int:
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    processor = Processor()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        with open(args.output_csv, 'w') as f:
            return processor.run(
                args.input_tiff_file,
                f,
            )
    except ImageNotFoundError as e:
        logging.error('Input image not found or is not readable.')
        return 1
    except TiffLoadError as e:
        logging.error('Input image is not valid TIFF image.')
        return 1
    except IOError as e:
        logging.error('Cannot open output file for writing.')
        return 2
    except Exception as e:
        logging.error('Unknown error occurred: {}'.format(e))
        return 255


if __name__ == '__main__':
    exit(main())
