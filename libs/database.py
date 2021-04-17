"""SQL System"""
from threading import local
from time import time

from peewee import BigAutoField
from peewee import DatabaseProxy
from peewee import Metadata
from peewee import Model
from peewee import TimestampField
from playhouse.pool import PooledMySQLDatabase
from playhouse.pool import PooledSqliteDatabase

from data import PROGRAMCONFIGLOCATION
from data.config import CONFIG
from libs import classproperty


# http://docs.peewee-orm.com/en/latest/peewee/installation.html


class Database:
    """SQL System"""

    __db = DatabaseProxy()

    @classmethod
    def setup(cls):
        """sets up the SQL System"""
        if CONFIG["database"]["mode"].value.lower() == "sqlite3":
            database = PooledSqliteDatabase(
                PROGRAMCONFIGLOCATION + "/Tackem.db",
                max_connections=20,
                timeout=0,
                pragmas={"journal_mode": "wal", "foreign_keys": 1},
            )
        elif CONFIG["database"]["mode"].lower() == "mysql":
            database = PooledMySQLDatabase(
                CONFIG["database"]["database"].value,
                max_connections=20,
                timeout=0,
                user=CONFIG["database"]["username"].value,
                password=CONFIG["database"]["password"].value,
                host=CONFIG["database"]["host"].value,
                port=CONFIG["database"]["port"].value,
            )
        else:
            print(CONFIG["database"]["mode"].value)

        cls.__db.initialize(database)

    @classproperty
    def db(cls) -> DatabaseProxy:
        """returns the DB"""
        return cls.__db


class ThreadSafeDatabaseMetadata(Metadata):
    def __init__(self, *args, **kwargs):
        # database attribute is stored in a thread-local.
        self._local = local()
        super(ThreadSafeDatabaseMetadata, self).__init__(*args, **kwargs)

    def _get_db(self):
        return getattr(self._local, "database", self._database)

    def _set_db(self, db):
        self._local.database = self._database = db

    database = property(_get_db, _set_db)


class TableBase(Model):
    """Base Table with Hard Delete"""

    id = BigAutoField()
    created_at = TimestampField(default=time)
    updated_at = TimestampField(default=0)

    class Meta:
        """Base Meta Data"""

        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata

    @classmethod
    def do_create(cls):
        return cls.create()

    @classmethod
    def do_update(cls, __data=None, **update):
        return cls.update(__data=__data, **update)

    @classmethod
    def do_delete(cls):
        return cls.delete()

    @classmethod
    def do_select(cls, *fields):
        return cls.select(*fields)


class SoftTableBase(TableBase):
    """Base Table with Soft Delete"""

    deleted_at = TimestampField(default=0)

    class Meta:
        """Base Meta Data"""

        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata

    @classmethod
    def do_update(cls, __data=None, **update):
        return cls.update(__data=__data, updated_at=time, **update).where(cls.deleted_at == 0)

    @classmethod
    def do_delete(cls):
        return cls.update(deleted_at=time)

    @classmethod
    def do_select(cls, *fields):
        return cls.select(*fields).where(cls.deleted_at == 0)
