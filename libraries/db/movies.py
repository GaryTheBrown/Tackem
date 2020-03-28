'''Library Movies Table'''
from libs.sql.table import Table
from libs.sql.column import Column

LIBRARY_MOVIE_DB_INFO = Table(
    "library_movies_{}_",
    1,
    Column(
        "id",
        "integer",
        primary_key=True,
        not_null=True
    ),
    Column(
        "fileid",
        "integer",
        not_null=True
    ),
    Column(
        "added",
        "datetime",
        not_null=True,
        default="CURRENT_TIMESTAMP",
        default_raw=True
    ),
    Column(
        "imdb",
        "varchar(9)",
        default="NULL",
        default_raw=True
    )
)
