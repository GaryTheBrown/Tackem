'''Library Files Table'''
from libs.sql.table import Table
from libs.sql.column import Column

LIBRARY_FILES_DB_INFO = Table(
    "library_files",
    1,
    Column(
        "id",
        "integer",
        primary_key=True,
        not_null=True
    ),
    Column(
        "filename",
        "text",
        not_null=True
    ),
    Column(
        "added",
        "datetime",
        not_null=True,
        default="CURRENT_TIMESTAMP",
        default_raw=True
    )
)
