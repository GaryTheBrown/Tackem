"""Post Upload Table"""
from peewee import BigIntegerField
from peewee import TextField

from libs.database import Database
from libs.database import SoftTableBase
from libs.database import ThreadSafeDatabaseMetadata


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
