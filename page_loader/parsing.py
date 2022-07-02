import argparse
import os


def parsing():
    parser = argparse.ArgumentParser(
        description='Download page')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=os.getcwd())
    args = vars(parser.parse_args())
    return args
