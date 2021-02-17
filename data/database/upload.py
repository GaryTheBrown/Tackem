'''Ripper Tables'''
from libs.database.table import Table
from libs.database.column import Column

UPLOAD_DB_INFO = Table(
    "upload",
    1,
    Column("key", "text", not_null=True),
    Column("filename", "text", not_null=True),
    Column("system", "text", not_null=True)
)
