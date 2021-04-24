"""Ripper Video Convert Info Table"""
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField

from database import SoftTableBase
from database.ripper.video_info import RipperVideoInfo


class RipperVideoConvertInfo(SoftTableBase):
    """Ripper Video Convert Info Table"""

    disc_info = ForeignKeyField(RipperVideoInfo, field="id", backref="convert_tracks")
    track_number = IntegerField()
    filename = TextField()
    label = TextField()
