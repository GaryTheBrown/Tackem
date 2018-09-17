'''Startup Arguments Setup'''
import argparse
import os.path

PROGRAMNAME = "Tackem"
PROGRAMVERSION = "ALPHA"

def parse():
    '''parses the command line arguments'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--home',
                        help="Change the home folder location",
                        default=os.path.expanduser("~/" + PROGRAMNAME + "/")
                       )
    parser.add_argument('--name',
                        help="Change the Programs Name",
                        default=PROGRAMNAME
                       )
    parser.add_argument('--version',
                        action='version',
                        version=PROGRAMNAME + " Version: " + PROGRAMVERSION)
    return parser.parse_args()

ARGS = parse()
