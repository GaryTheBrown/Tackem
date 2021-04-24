"""Library Files Table"""
from peewee import BlobField
from peewee import BooleanField
from peewee import TextField
from peewee import TimestampField

from database import SoftTableBase


class LibraryFile(SoftTableBase):
    """Library Files Table"""

    folder = TextField()
    filename = TextField()
    # type = CharField(max_length=16)
    checksum = BlobField()
    last_check = TimestampField()
    bad_file = BooleanField(default=False)
    missing_file = BooleanField(default=False)
    # from_system = TextField()
    # from_id = IntegerField()
