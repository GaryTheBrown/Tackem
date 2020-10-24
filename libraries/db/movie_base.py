'''Library Movies Table'''
from libs.database.table import Table
from libs.database.column import Column

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
