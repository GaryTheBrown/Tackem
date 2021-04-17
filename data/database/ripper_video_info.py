"""Ripper Video Info Table"""
from peewee import BitField
from peewee import CharField
from peewee import TextField
from playhouse.sqlite_ext import JSONField

from libs.database import Database
from libs.database import TableBase
from libs.database import ThreadSafeDatabaseMetadata


class VideoInfo(TableBase):
    """Ripper Video Info Table"""

    iso_file = TextField(default="")
    uuid = CharField(max_length=16)
    label = TextField()
    disc_type = CharField(max_length=6)
    disc_data = JSONField()
    rip_data = JSONField()
    rip_data_locked = BitField(default=False)

    class Meta:
        table_name = "ripper_video_info"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
