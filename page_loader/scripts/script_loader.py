#!/usr/bin/env python

from page_loader.download import download
from page_loader.parsing import parsing
import logging
import sys


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.INFO)
    stderr_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('loader.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stderr_handler)

    args = parsing()
    download(args['url'], args['output'])


if __name__ == '__main__':
    main()
