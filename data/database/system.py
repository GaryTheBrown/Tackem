"""Library Files Table"""
from libs.database.column import Column
from libs.database.table import Table

TABLE_VERSION_DB = Table(
    "table_version",
    0,
    Column("name", "text", not_null=True),
    Column("version", "integer", not_null=True),
)

UPLOAD_DB = Table(
    "post_upload",
    1,
    Column("key", "text", not_null=True),
    Column("filename", "text", not_null=True),
    Column("filesize", "bigint", not_null=True),
    Column("system", "text", not_null=True),
    # TODO system id column so when passing data to the library it knows what is being passed easier
    soft_delete=True,
)
