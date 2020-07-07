'''Library Movies Table'''
from libs.sql.table import Table
from libs.sql.column import Column

LIBRARY_MOVIES_DB_INFO = Table(
    "library_movies",
    1,
    Column(
        "fileid",
        "integer"
    ),
    Column(
        "imdb",
        "varchar(9)",
        default="NULL",
        default_raw=True
    )
)
