'''File and Folder functions'''
import pathlib
from data import PROGRAMCONFIGLOCATION
from data.config import CONFIG

class File:
    '''Class full of file functions'''
    @classmethod
    def mkdir(cls, folder: str, root=PROGRAMCONFIGLOCATION):
        '''creates a folder if it doesn't exist'''
        if folder[0] != "/":
            folder = root + folder
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
