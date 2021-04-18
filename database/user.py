"""User Table"""
from peewee import BooleanField
from peewee import TextField

from database import Database
from database import TableBase
from database import ThreadSafeDatabaseMetadata


class User(TableBase):
    """User Table"""

    username = TextField(unique=True)
    password = TextField()
    is_admin = BooleanField(default=0)

    class Meta:
        table_name = "users"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
