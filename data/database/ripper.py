'''Ripper Tables'''
from libs.database.column import Column
from libs.database.table import Table

AUDIO_INFO_DB = Table(
    "ripper_audio_info",
    1,
    Column("iso_file", "text", default=""),
    Column("musicbrainz_disc_id", "varchar(28)", not_null=True),
    Column("track_count", "tinyint", not_null=True),
    Column("release_id", "varchar(36)", not_null=True),
    Column("disc_data", "json")
)

VIDEO_CONVERT_DB = Table(
    "ripper_video_convert_info",
    1,
    Column("info_id", "integer", not_null=True),
    Column("filename", "text", not_null=True),
    Column("disc_info", "json"),
    Column("track_data", "json"),
    Column("ripper_video_info_id", "bit", not_null=True, default=False)
)

VIDEO_INFO_DB = Table(
    "ripper_video_info",
    1,
    Column("iso_file", "text", default=""),
    Column("uuid", "varchar(16)", default=""),
    Column("label", "text", default=""),
    Column("disc_type", "varchar(6)", default=""),
    Column("rip_data", "json")
)
