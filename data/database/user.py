"""User Table"""
from peewee import BitField
from peewee import TextField

from libs.database import Database
from libs.database import TableBase
from libs.database import ThreadSafeDatabaseMetadata


class User(TableBase):
    """User Table"""

    username = TextField(unique=True)
    password = TextField()
    is_admin = BitField(default=False)

    class Meta:
        table_name = "users"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
