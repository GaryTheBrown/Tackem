"""User Table"""
from peewee import BooleanField
from peewee import TextField

from database import TableBase


class User(TableBase):
    """User Table"""

    username = TextField(unique=True)
    password = TextField()
    is_admin = BooleanField(default=0)
