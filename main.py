# coding=utf-8
import glob
from argparse import ArgumentParser

from unit.processor import Processor


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()

    return parser


def main() -> int:
    processor = Processor(
        glob.glob('data/*.tif'),  # sys.argv[1:],
        './'
    )

    return processor.run()


if __name__ == '__main__':
    exit(main())
