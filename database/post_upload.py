"""Post Upload Table"""
from peewee import BigIntegerField
from peewee import TextField

from database import SoftTableBase


class PostUpload(SoftTableBase):
    """Post Upload Table"""

    key = TextField()
    filename = TextField()
    filesize = BigIntegerField()
    system = TextField()
