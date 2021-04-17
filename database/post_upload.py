"""Post Upload Table"""
from peewee import BigIntegerField
from peewee import TextField

from database import Database
from database import SoftTableBase
from database import ThreadSafeDatabaseMetadata


class PostUpload(SoftTableBase):
    """Post Upload Table"""

    key = TextField()
    filename = TextField()
    filesize = BigIntegerField()
    system = TextField()

    class Meta:
        table_name = "post_upload"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
