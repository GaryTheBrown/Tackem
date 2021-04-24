"""Ripper Audio Info Table"""
from peewee import CharField
from peewee import SmallIntegerField
from peewee import TextField
from playhouse.sqlite_ext import JSONField

from database import TableBase


class RipperAudioInfo(TableBase):
    """Ripper Audio Info Table"""

    iso_file = TextField(null=True, default="")
    musicbrainz_disc_id = (CharField(max_length=28),)
    track_count = SmallIntegerField()
    release_id = CharField(max_length=36)
    disc_data = JSONField()
