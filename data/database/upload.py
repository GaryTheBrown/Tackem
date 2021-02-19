'''Ripper Tables'''
from libs.database.column import Column
from libs.database.table import Table

UPLOAD_DB_INFO = Table(
    "upload",
    1,
    Column("key", "text", not_null=True),
    Column("filename", "text", not_null=True),
    Column("system", "text", not_null=True)
)
