'''Database Config'''
from libs.config.list import ConfigList
from libs.config.obj.integer_number import ConfigObjIntegerNumber
from libs.config.obj.password import ConfigObjPassword
from libs.config.obj.string import ConfigObjString
from libs.config.obj.data.input_attributes import InputAttributes
from libs.config.obj.data.radio import ConfigObjRadio
from libs.config.obj.options.radio import ConfigObjOptionsRadio

def database_config() -> ConfigList:
    '''Database Config'''
    return ConfigList(
        "database",
        "Database",
        ConfigObjOptionsRadio(
            "mode",
            [
                ConfigObjRadio(
                    "sqlite3",
                    "SQLite3",
                    input_attributes=InputAttributes(
                        data_click_hide="database_mysql_section"
                    )
                ),
                ConfigObjRadio(
                    "mysql",
                    "MYSQL",
                    input_attributes=InputAttributes(
                        disabled=True,
                        data_click_show="database_mysql_section"
                    )
                )
            ],
            "sqlite3",
            "Database Mode",
            "What system do you want to use for data?"
        ),
        ConfigList(
            "mysql",
            "MYSQL",
            ConfigObjString(
                "host",
                "localhost",
                "Database Address",
                "The Database Address Name or IP"
            ),
            ConfigObjIntegerNumber(
                "port",
                3306,
                "Database Port",
                "The port your database is open on",
                input_attributes=InputAttributes(
                    min=1001,
                    max=65535
                )
            ),
            ConfigObjString(
                "username",
                "",
                "Database Username",
                "The username for access to the database"
            ),
            ConfigObjPassword(
                "password",
                "Database Password",
                "The password for access to the database"
            ),
            ConfigObjString(
                "database",
                "tackem",
                "Database Name",
                "The name of the database"
            ),
            is_section=True
        )
    )
