'''Library Files Table'''
from libs.sql.table import Table
from libs.sql.column import Column

LIBRARY_FILES_DB_INFO = Table(
    "library_files",
    1,
    Column(
        "folder",
        "text",
        not_null=True
    ),
    Column(
        "filename",
        "text",
        not_null=True
    ),
    Column(
        "type",
        "varchar",
        size=16,
        not_null=True
    ),
    Column(
        "checksum",
        "binary",
        size=32
    ),
    Column(
        "last_check",
        "bigint" # unix timestamp
    ),
    Column(
        "bad_file",
        "bit",
        default=0
    ),
    Column(
        "missing_file",
        "bit",
        default=0
    ),
    Column(
        "from_system",
        "text",
    ),
    Column(
        "from_id",
        "integer"
    ),
)
