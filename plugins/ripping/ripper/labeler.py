'''Master Section for the Labeler controller'''
import json
from .converter import create_converter_row
from .data.events import RipperEvents
from .data.db_tables import VIDEO_INFO_DB_INFO as INFO_DB
from .data.disc_type import DiscType

class Labeler():
    '''Master Section for the Drive controller'''
    def __init__(self, db, config):
        self._db = db
        self._config = config

##############
##HTML STUFF##
##############
    def get_data(self, thread_name):
        '''returns the data as json or dict for html'''
        dict_of_values = {"ripped":True, "ready_to_convert":False, "ready_to_rename":False}
        return self._db.select(thread_name, INFO_DB["name"], dict_of_values)

    def get_data_by_id(self, thread_name, db_id):
        '''returns the data as json or dict for html'''
        data = self._db.select_by_row(thread_name, INFO_DB["name"], db_id)
        if data["ripped"] is False:
            return False
        if data["ready_to_convert"] is True:
            return False
        if data["ready_to_rename"] is True:
            return False
        return data

    def set_data(self, thread_name, db_id, data, finished=False):
        '''Sets Data Back in the Database'''
        if isinstance(data, DiscType):
            dict_for_db = {"rip_data":json.dumps(data.make_dict())}
            if finished:
                if self._config['converter']['enabled']:
                    create_converter_row(self._db, thread_name, db_id, data,
                                         self._config['videoripping']['torip'])
                    dict_for_db["ready_to_convert"] = True
                else:
                    dict_for_db["ready_to_rename"] = True

            if finished:
                if self._config['converter']['enabled']:
                    RipperEvents().converter.set()
                else:
                    RipperEvents().renamer.set()
