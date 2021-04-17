"""Library Files Table"""
from peewee import BitField
from peewee import BlobField
from peewee import CharField
from peewee import IntegerField
from peewee import TextField
from peewee import TimestampField

from database import Database
from database import SoftTableBase
from database import ThreadSafeDatabaseMetadata


class LibraryFiles(SoftTableBase):
    """Library Files Table"""

    folder = TextField()
    filename = TextField()
    type = CharField(max_length=16)
    checksum = BlobField()
    last_check = TimestampField()
    bad_file = BitField(default=False)
    missing_file = BitField(default=False)
    from_system = TextField()
    from_id = IntegerField()

    class Meta:
        table_name = "library_files"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
