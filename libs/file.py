"""File and Folder functions"""
import os
import pathlib
import shutil
import time

from data import PROGRAMCONFIGLOCATION


class File:
    """Class full of file functions"""

    @staticmethod
    def location(folder: str, root: str = PROGRAMCONFIGLOCATION) -> str:
        """returns the absolute location"""
        if folder[0] != "/":
            if root[0] != "/":
                folder = File.location(root) + folder
            else:
                folder = root + folder
        return folder

    @staticmethod
    def mkdir(folder: str, root: str = PROGRAMCONFIGLOCATION):
        """creates a folder if it doesn't exist"""
        if folder[0] != "/":
            folder = root + folder
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def move(source: str, destination: str):
        """Moves file from one place to another destiniation must contain the filename too"""
        shutil.move(source, destination)

    @staticmethod
    def rm(file: str):
        """remove a file"""
        if File.exists(file):
            os.remove(file)

    @staticmethod
    def rmdir(folder: str, recursive: bool = False):
        """remove a folder"""
        if not recursive:
            if File.exists(folder):
                os.rmdir(folder)
            return
        if File.exists(folder):
            for path in pathlib.Path(folder).rglob("*"):
                if os.path.isfile(path):
                    File.rm(path)
                elif os.path.isdir(path):
                    File.rmdir(path)

    @staticmethod
    def touch(file: str):
        """creates an empty file"""
        pathlib.Path(file).touch()

    @staticmethod
    def exists(file_or_folder: str) -> bool:
        """checks if a file or folder exists"""
        return os.path.exists(file_or_folder)

    @staticmethod
    def wait_for_file_copy_complete(file):
        """watches the file size until it stops"""
        filename = File.location(file)
        historicalSize = -1
        while historicalSize != os.path.getsize(filename):
            historicalSize = os.path.getsize(filename)
            time.sleep(4)
