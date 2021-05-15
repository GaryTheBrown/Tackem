"""Library Files Table"""
from __future__ import annotations  # TODO drop this when we hit python 3.10

import datetime
import hashlib
import time
from pathlib import Path
from typing import List
from typing import Optional

from peewee import BlobField
from peewee import BooleanField
from peewee import FixedCharField
from peewee import TextField
from peewee import TimestampField

from config import CONFIG
from database import SoftTableBase
from libs.file import File


class LibraryFile(SoftTableBase):
    """Library Files Table"""

    __BLOCKSIZE = 65536

    library = FixedCharField(max_length=20)
    folder = TextField()
    filename = TextField()
    checksum = BlobField()
    last_check = TimestampField()
    bad_file = BooleanField(default=False)
    missing_file = BooleanField(default=False)

    @classmethod
    def files_to_check(cls) -> Optional[List[LibraryFile]]:
        """Threadded Script For running"""
        regularity = CONFIG["libraries"]["autofilecheck"]["regularity"].value

        if regularity == "disabled":
            return None

        now = datetime.datetime.now()
        if regularity == "hourly":
            from_before = now + datetime.timedelta(hours=-1)
        elif regularity == "daily":
            from_before = now + datetime.timedelta(days=-1)
        elif regularity == "weekly":
            from_before = now + datetime.timedelta(weeks=-1)
        elif regularity == "monthly":
            from_before = now + datetime.timedelta(months=-1)
        elif regularity == "quaterly":
            from_before = now + datetime.timedelta(months=-3)
        elif regularity == "halfyear":
            from_before = now + datetime.timedelta(months=-6)
        elif regularity == "year":
            from_before = now + datetime.timedelta(years=-1)

        return cls.do_select().where(LibraryFile.last_check < from_before)

    @classmethod
    def scan_folder_base(cls, library: str):
        """Scans the folder for new files"""
        for path in Path(File.location(CONFIG["libraries"][library]["location"].value)).rglob("*"):
            ext = path.parts[-1].split(".")[-1]
            if ext not in CONFIG["libraries"][library]["extensions"].value:
                continue

            folder = path.joinpath().replace(path.name, "")
            existing = LibraryFile.get_or_none(
                LibraryFile.folder == folder, LibraryFile.filename == path.name
            )
            if existing:
                continue

            new_file = LibraryFile()
            new_file.library = library[0].upper()
            new_file.folder = folder
            new_file.filename = path.name
            new_file.checksum = new_file.get_file_checksum()
            new_file.last_check = int(time.time())
            new_file.save()

    @property
    def file_path(self):
        """returns the full file path"""
        return (
            File.location(CONFIG["libraries"][self.library]["location"].value)
            + self.folder
            + self.filename
        )

    def get_file_checksum(self) -> str:
        """Creates checksum hash for a file in Binary from SHA256"""

        hasher = hashlib.sha256()
        with open(self.file_path, "rb") as open_file:
            buffer = open_file.read(self.__BLOCKSIZE)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = open_file.read(self.__BLOCKSIZE)
        return hasher.digest()

    def check_file(self) -> bool:
        """Check File has not gone bad"""
        if Path(self.file_path).is_file():
            checksum = self.get_file_checksum()
            if checksum == self.checksum:
                self.last_check = int(time.time())
                self.save()
                return True

            print(f"FILE HAS GONE BAD {self.file_path}")
            self.bad_file = True
            self.checksum = checksum
        else:
            self.missing_file = True
        self.save()
        return False
