'''File and Folder functions'''
import pathlib
from data import PROGRAMCONFIGLOCATION
class File:
    '''Class full of file functions'''

    @classmethod
    def location(cls, folder: str, root: str = PROGRAMCONFIGLOCATION ) -> str:
        '''returns the absolute location'''
        if folder[0] != "/":
            folder = root + folder
        return folder

    @classmethod
    def mkdir(cls, folder: str, root: str = PROGRAMCONFIGLOCATION):
        '''creates a folder if it doesn't exist'''
        if folder[0] != "/":
            folder = root + folder
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
