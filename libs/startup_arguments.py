'''Startup Arguments Setup'''
import argparse
import os.path
import sys
PROGRAMVERSION = "ALPHA"
PROGRAMCONFIGLOCATION = "~/.Tackem/"

if sys.platform == "win32":
    PROGRAMCONFIGLOCATION = os.environ['APPDATA'] + "/Tackem/"

def parse():
    '''parses the command line arguments'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--home',
                        help="Change the home folder location",
                        default=os.path.expanduser(PROGRAMCONFIGLOCATION)
                       )
    parser.add_argument('--version',
                        action='version',
                        version="Tackem Version: " + PROGRAMVERSION)
    return parser.parse_args()

ARGS = parse()
