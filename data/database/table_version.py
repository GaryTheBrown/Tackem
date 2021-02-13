'''Library Files Table'''
from libs.database.table import Table
from libs.database.column import Column

TABLE_VERSION_DB_INFO = Table(
    "table_version",
    0,
    Column(
        "name",
        "text",
        not_null=True
    ),
    Column(
        "version",
        "integer",
        not_null=True
    ),
)
