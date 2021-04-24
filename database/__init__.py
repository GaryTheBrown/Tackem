"""SQL System"""
import time

from peewee import BigAutoField
from peewee import CharField
from peewee import DatabaseProxy
from peewee import IntegerField
from peewee import Model
from peewee import MySQLDatabase
from peewee import TimestampField
from playhouse.migrate import migrate
from playhouse.migrate import MySQLMigrator
from playhouse.migrate import SchemaMigrator
from playhouse.migrate import SqliteMigrator
from playhouse.sqlite_ext import SqliteExtDatabase

from config import CONFIG
from data import PROGRAMCONFIGLOCATION
from libs import classproperty


# http://docs.peewee-orm.com/en/latest/peewee/installation.html
# To Do Schema Updates you need to create a list of operations and a that list to the tables
# migration function as a new list in the main list
# http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations


class Database:
    """SQL System"""

    __db = DatabaseProxy()
    __migrator = None

    @classmethod
    def setup(cls):
        """sets up the SQL System"""
        mode = CONFIG["database"]["mode"].value.lower()
        if mode == "sqlite3":
            database = SqliteExtDatabase(
                PROGRAMCONFIGLOCATION + "/Tackem.db",
                pragmas={"journal_mode": "wal", "foreign_keys": 0},
            )

        elif mode == "mysql":
            database = MySQLDatabase(
                CONFIG["database"]["database"].value,
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
        # with Database.db.connection_context():
        TableVersion.create_table()

    @classproperty
    def db(cls) -> DatabaseProxy:
        """returns the DB"""
        return cls.__db

    @classproperty
    def migrator(cls) -> SchemaMigrator:
        """returns the migrator"""
        return cls.__migrator


class BaseModel(Model):
    class Meta:
        database = Database.db
        legacy_table_names = False


class TableVersion(BaseModel):
    """table to keep track of table versions"""

    name = CharField(max_length=60, index=True)
    version = IntegerField(default=0)


class TableBase(BaseModel):
    """Base Table with Hard Delete"""

    def inttime():
        return int(time.time())

    id = BigAutoField()
    created_at = TimestampField(default=inttime)
    updated_at = TimestampField(default=0)

    @classmethod
    def do_create(cls):
        return cls.create()

    @classmethod
    def do_update(cls, __data=None, **update):
        if isinstance(__data, dict):
            __data["updated_at"] = time
            return cls.update(__data=__data, **update)
        else:
            return cls.update(__data=__data, updated_at=int(time.time()), **update)

    @classmethod
    def do_delete(cls):
        return cls.delete()

    @classmethod
    def do_select(cls, *fields):
        return cls.select(*fields)

    def save(self, force_insert=False, only=None):
        self.updated_at = int(time.time())
        return super().save(force_insert, only)

    @classmethod
    def migrations(cls):
        """No Migrations"""
        return []

    @classmethod
    def table_setup(cls) -> bool:
        """Magic to create the table returns true if a table is created"""
        tv = TableVersion.get_or_none(name=cls._meta.table_name)
        if not cls.table_exists():
            cls.create_table()
            tv = TableVersion()
            tv.name = cls._meta.table_name
            tv.version = 0
            tv.save()
            return True
        else:
            migrations = cls.migrations()
            if migrations == []:
                tv.version = 0
            else:
                current_version = tv.version - 1
                with Database.db.atomic():
                    for migration in migrations[current_version:]:
                        migrate(*migration)

            tv.version = len(migrations) if isinstance(migrations, list) else 0
            tv.save()
            return False


class SoftTableBase(TableBase):
    """Base Table with Soft Delete"""

    deleted_at = TimestampField(default=0)

    @classmethod
    def do_update(cls, __data=None, **update):
        if isinstance(__data, dict):
            __data["updated_at"] = int(time.time())
            return cls.update(__data=__data, **update).where(cls.deleted_at == 0)
        else:
            return cls.update(__data=__data, updated_at=int(time.time()), **update).where(
                cls.deleted_at == 0
            )

    @classmethod
    def do_delete(cls):
        return cls.update({"deleted_at": int(time.time())})

    @classmethod
    def do_select(cls, *fields):
        return cls.select(*fields).where(cls.deleted_at == 0)
