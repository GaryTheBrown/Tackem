'''Database Table'''
from typing import Any, List
from libs.database.column import Column


class Table:
    '''Database Table'''

    def __init__(self, name: str, version: int, *data: Column, soft_delete: bool = False):
        self.__name = name
        self.__version = version
        self.__data = list(data)
        self.__soft_delete = soft_delete

        self.__main_data = [
            Column(
                "id",
                "integer",
                primary_key=True,
                auto_increment=True
            ),
            Column(
                "created_at",
                "timestamp",
                default="CURRENT_TIMESTAMP",
                default_raw=True
            ),
            Column(
                "updated_at",
                "timestamp",
                default=0,
            ),
        ]
        if self.__soft_delete:
            self.__main_data.append(
                Column(
                    "deleted_at",
                    "timestamp",
                    default=0
                )
            )

    def name(self, *values: Any) -> str:
        '''returns the name'''
        if "{}" in self.__name and values is None:
            ValueError("Tried to get DB Name but missing values")
        if values:
            return self.__name.format(*values)
        return self.__name

    @property
    def version(self):
        '''returns the version'''
        return self.__version

    @property
    def data(self):
        '''returns data'''
        return self.__main_data + self.__data

    @property
    def soft_delete(self):
        '''returns if soft delete'''
        return self.__soft_delete

    @property
    def keys(self):
        '''return a list of keys'''
        return [column.name for column in self.data]

    def check_value(self, key: str, value: Any):
        '''checks the dict of values against the Columns fails on first bad value'''
        for column in self.__main_data + self.__data:
            if column.name == key:
                column.check_value(value)
                return
        raise ValueError(f"{key} not found in {self.__name}")

    def check_values(self, values: dict):
        '''checks the dict of values against the Columns fails on first bad value'''
        for key, value in values.items():
            found = False
            for column in self.__main_data + self.__data:
                if column.name == key:
                    column.check_value(value)
                    found = True
                    break
            if not found:
                raise ValueError(f"{key} not found in {self.__name}")

    def has_column(self, column_name: str) -> bool:
        '''checks if the table has a column by name'''
        for column in self.__main_data + self.__data:
            if column.name == column_name:
                return True
        return False

    @property
    def columns(self) -> list:
        '''returns the columns data for creation'''
        return [column.create_string() for column in self.data]
