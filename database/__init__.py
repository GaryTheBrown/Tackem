"""SQL System"""
from threading import local
from time import time
from typing import Union

from peewee import BigAutoField
from peewee import CharField
from peewee import DatabaseProxy
from peewee import DoesNotExist
from peewee import IntegerField
from peewee import Metadata
from peewee import Model
from peewee import TimestampField
from playhouse.migrate import migrate
from playhouse.migrate import MySQLMigrator
from playhouse.migrate import SqliteMigrator
from playhouse.pool import PooledMySQLDatabase
from playhouse.pool import PooledSqliteDatabase

from config import CONFIG
from data import PROGRAMCONFIGLOCATION
from libs import classproperty


# http://docs.peewee-orm.com/en/latest/peewee/installation.html


class Database:
    """SQL System"""

    __db = DatabaseProxy()
    __migrator = None

    @classmethod
    def setup(cls):
        """sets up the SQL System"""
        mode = CONFIG["database"]["mode"].value.lower()
        if mode == "sqlite3":
            database = PooledSqliteDatabase(
                PROGRAMCONFIGLOCATION + "/Tackem.db",
                max_connections=20,
                timeout=0,
                pragmas={"journal_mode": "wal", "foreign_keys": 0},
            )

        elif mode == "mysql":
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
            print(mode)

        cls.__db.initialize(database)

        if mode == "sqlite3":
            cls.__migrator = SqliteMigrator(cls.__db)
        elif mode == "mysql":
            cls.__migrator = MySQLMigrator(cls.__db)

        TableVersion.create_table()

    @classproperty
    def db(cls) -> DatabaseProxy:
        """returns the DB"""
        return cls.__db

    @classproperty
    def migrator(cls) -> Union[MySQLMigrator, SqliteMigrator]:
        """returns the migrator"""
        return cls.__migrator


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


class TableVersion(Model):
    """table to keep track of table versions"""

    name = CharField(max_length=60, index=True)
    version = IntegerField(default=0)

    class Meta:
        """Base Meta Data"""

        table_name = "table_versions"
        database = Database.db
        model_metadata_class = ThreadSafeDatabaseMetadata


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

    def save(self, force_insert=False, only=None):
        self.updated_at = time
        return super().save(force_insert, only)

    @classmethod
    def migrations(cls):
        """No Migrations"""
        return []

    @classmethod
    def table_setup(cls):  # , migrations: Optional[list] = None):
        """Magic to create the table"""
        try:
            tv = TableVersion.get(TableVersion.name == cls._meta.table_name)
        except DoesNotExist:
            tv = TableVersion()
            tv.name = cls._meta.table_name

        migrations = cls.migrations()

        if not cls.table_exists():
            cls.create_table()
        else:
            # migrations = cls._migrations()
            if migrations == []:
                tv.version = 0
            else:
                current_version = tv.version - 1
                with Database.db.atomic():
                    for migration in migrations[current_version:]:
                        migrate(*migration)

            tv.version = len(migrations) if isinstance(migrations, list) else 0
            tv.save()


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
