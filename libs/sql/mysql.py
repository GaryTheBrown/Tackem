'''MariaDB System'''
from .baseclass import SqlBaseClass

class MySql(SqlBaseClass):
    '''mariabd system'''

    def __startup(self):
        '''Setup the System Here'''

    def __shutdown(self):
        '''Shutdown the System Here'''

    ###########
    ##PRIVATE##
    ###########

    def __check_version_table_exists(self):
        '''returns if the table_version exists'''
        command = 'SELECT * FROM Tackem'
        command += '.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = "table_version"'
        return bool(self.__trusted_get(command, False))

    def __trusted_call(self, call):
        '''Trusted Calls can send the command in a string to here for execution'''

    def __trusted_get(self, call, return_dict=True):
        '''Grab a list of the tables'''

    def __update_table(self, table_name, data, version):
        '''Update the table with the informaiton provided'''

    ##########
    ##PUBLIC##
    ##########
