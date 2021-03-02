'''Ripper Tables'''
from libs.database.column import Column
from libs.database.table import Table

AUDIO_CONVERT_DB = Table(
    "ripping_ripper_audio_convert_info",
    1,
    Column("info_id", "integer", not_null=True),
    Column("filename", "text", not_null=True),
    Column("track_info", "json"),
    Column("converted", "bit", not_null=True, default=False)
)

AUDIO_INFO_DB = Table(
    "ripping_ripper_audio_info",
    1,
    Column("iso_file", "text", default=""),
    Column("musicbrainz_disc_id", "varchar(28)", not_null=True),
    Column("track_count", "tinyint", not_null=True),
    Column("release_id", "varchar(36)", not_null=True),
    Column("disc_data", "json"),
    Column("ripped", "bit", not_null=True, default=False),
    Column("ready_to_convert", "bit", not_null=True, default=False),
    Column("ready_to_rename", "bit", not_null=True, default=False),
    Column("ready_for_library", "bit", not_null=True, default=False),
    Column("completed", "bit", not_null=True, default=False),
)

VIDEO_CONVERT_DB = Table(
    "ripping_ripper_video_convert_info",
    1,
    Column("info_id", "integer", not_null=True),
    Column("filename", "text", not_null=True),
    Column("disc_info", "json"),
    Column("track_data", "json"),
    Column("converted", "bit", not_null=True, default=False)
)

VIDEO_INFO_DB = Table(
    "ripping_ripper_video_info",
    1,
    Column("iso_file", "text", default=""),
    Column("uuid", "varchar(16)", default=""),
    Column("label", "text", default=""),
    Column("disc_type", "varchar(6)", default=""),
    Column("rip_data", "json"),
    Column("ripped", "bit", not_null=True, default=False),
    Column("ready_to_convert", "bit", not_null=True, default=False),
    Column("ready_to_rename", "bit", not_null=True, default=False),
    Column("ready_for_library", "bit", not_null=True, default=False),
    Column("completed", "bit", not_null=True, default=False)
)
