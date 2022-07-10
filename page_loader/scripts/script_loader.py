#!/usr/bin/env python

from page_loader.download import download
from page_loader.parsing import parsing
import logging  


def main():
    logging.basicConfig(filename='loader.log',
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                level=logging.DEBUG,
                )
    logging.info('Loader started')
    args = parsing()
    download(args['url'], args['output'])
    logging.info('Loader finished')


if __name__ == '__main__':
    main()
