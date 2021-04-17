"""Ripper Video Convert Info Table"""
from peewee import BitField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField
from playhouse.sqlite_ext import JSONField

from database import Database
from database import SoftTableBase
from database import ThreadSafeDatabaseMetadata
from database.ripper_video_info import VideoInfo


class VideoConvertInfo(SoftTableBase):
    """Ripper Video Convert Info Table"""

    disc_info = ForeignKeyField(VideoInfo, field="id", backref="convert_tracks")
    track_number = IntegerField()
    filename = TextField()
    label = TextField()
    track_data = JSONField()
    video_converted = BitField(default=False)

    class Meta:
        table_name = "ripper_video_convert_info"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
