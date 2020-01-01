'''Startup Arguments Setup'''
import argparse
import os.path
HOMEFOLDER = os.path.expanduser("~")
PROGRAMNAME = "Tackem"
PROGRAMVERSION = "ALPHA"
PROGRAMGITADDRESS = "http://github.com/garythebrown/tackem/"
PROGRAMCONFIGLOCATION = HOMEFOLDER + "/.Tackem/"
PLUGINFOLDERLOCATION = "plugins/"
THEMEFOLDERLOCATION = "themes/"


def __parse():
    '''parses the command line arguments'''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--version',
                        action='version',
                        version="Tackem Version: " + PROGRAMVERSION)
    return parser.parse_args()


ARGS = __parse()
