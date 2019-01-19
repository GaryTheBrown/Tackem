'''MariaDB System'''
from .baseclass import MysqlBaseClass

class MySql(MysqlBaseClass):
    '''mariabd system'''

    def __init__(self):
        '''Setup MariaDB connection here'''
        print("NOT COMPLETED WILL NOT WORK")

    def _startup(self):
        '''Setup the System Here'''
        pass

    def _shutdown(self):
        '''Shutdown the System Here'''
        pass

    ###########
    ##PRIVATE##
    ###########

    def _check_version_table_exists(self):
        '''returns if the table_version exists'''
        command = 'SELECT * FROM Tackem'
        command += '.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = "table_version"'
        return bool(self._trusted_get(command, False))

    def _trusted_call(self, call):
        '''Trusted Calls can send the command in a string to here for execution'''
        pass

    def _trusted_get(self, call, return_dict):
        '''Grab a list of the tables'''
        pass

    ##########
    ##PUBLIC##
    ##########
