'''Startup Arguments Setup'''
import argparse
from data import PROGRAMVERSION

# TODO reimplement this into the program as not used at all


def __parse():
    '''parses the command line arguments'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--version',
                        action='version',
                        version="Tackem Version: " + PROGRAMVERSION)
    return parser.parse_args()


ARGS = __parse()
