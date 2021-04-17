"""Ripper Audio Info Table"""
from peewee import CharField
from peewee import SmallIntegerField
from peewee import TextField
from playhouse.sqlite_ext import JSONField

from libs.database import Database
from libs.database import TableBase
from libs.database import ThreadSafeDatabaseMetadata


class AudioInfo(TableBase):
    """Ripper Audio Info Table"""

    iso_file = TextField(null=True, default="")
    musicbrainz_disc_id = (CharField(max_length=28),)
    track_count = SmallIntegerField()
    release_id = CharField(max_length=36)
    disc_data = JSONField()

    class Meta:
        table_name = "ripper_audio_info"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata
