'''MariaDB System'''
from libs.sql.baseclass import SqlBaseClass

class MySql(SqlBaseClass):
    '''mariabd system'''

    def _startup(self):
        '''Setup the System Here'''

    def _shutdown(self):
        '''Shutdown the System Here'''

    def _check_version_table_exists(self) -> bool:
        '''returns if the table_version exists'''
        cmd = 'SELECT * FROM Tackem.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = "table_version"'
        return bool(self._trusted_get(cmd, False))

    def _trusted_call(self, call):
        '''Trusted Calls can send the command in a string to here for execution'''

    def _trusted_get(self, call, return_dict=True) -> list:
        '''Grab a list of the tables'''

    def _update_table(self, table_name, data, version) -> bool:
        '''Update the table with the informaiton provided'''
