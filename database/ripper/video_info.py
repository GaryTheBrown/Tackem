"""Ripper Video Info Table"""
from peewee import BooleanField
from peewee import CharField
from peewee import TextField
from playhouse.sqlite_ext import JSONField

from database import TableBase


class RipperVideoInfo(TableBase):
    """Ripper Video Info Table"""

    iso_file = TextField(default="")
    uuid = CharField(max_length=16)
    label = TextField()
    disc_type = CharField(max_length=6)
    disc_data = JSONField()
    rip_data = JSONField()
    rip_data_locked = BooleanField(default=0)
    rip_data_downloaded = BooleanField(default=0)
