"""File and Folder functions"""
import os
import pathlib
import shutil

from data import PROGRAMCONFIGLOCATION


class File:
    """Class full of file functions"""

    @classmethod
    def location(cls, folder: str, root: str = PROGRAMCONFIGLOCATION) -> str:
        """returns the absolute location"""
        if folder[0] != "/":
            folder = root + folder
        return folder

    @classmethod
    def mkdir(cls, folder: str, root: str = PROGRAMCONFIGLOCATION):
        """creates a folder if it doesn't exist"""
        if folder[0] != "/":
            folder = root + folder
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    @classmethod
    def move(cls, source: str, destination: str):
        """Moves file from one place to another destiniation must contain the filename too"""
        shutil.move(source, destination)

    @classmethod
    def rm(cls, file: str):
        """remove a file"""
        if cls.exists(file):
            os.remove(file)

    @classmethod
    def rmdir(cls, folder: str, recursive: bool = False):
        """remove a folder"""
        if not recursive:
            if cls.exists(folder):
                os.rmdir(folder)
            return
        if cls.exists(folder):
            for path in pathlib.Path(folder).rglob("*"):
                if os.path.isfile(path):
                    cls.rm(path)
                elif os.path.isdir(path):
                    cls.rmdir(path)

    @classmethod
    def touch(cls, file: str):
        """creates an empty file"""
        pathlib.Path(file).touch()

    @classmethod
    def exists(cls, file_or_folder: str) -> bool:
        """checks if a file or folder exists"""
        return os.path.exists(file_or_folder)
