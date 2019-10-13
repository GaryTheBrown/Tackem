'''System Data'''
import threading


class SystemData():
    '''System Data'''


    __plugins = {} # [type][ name]
    __plugins_lock = threading.Lock()
    __systems = {} # [type name]
    __systems_lock = threading.Lock()
    __plugin_cfg = {} # [type name]
    __plugin_cfg_lock = threading.Lock()
    __config = None
    __config_lock = threading.Lock()
    __sql = None
    __auth = None
    __musicbrainz = None


    @property
    def plugins(self):
        '''returns the plugin [type][ name]'''
        return self.__plugins


    @property
    def plugins_lock(self):
        '''returns the plugins_lock'''
        return self.__plugins_lock


    @property
    def systems(self):
        '''returns the systems [type name]'''
        return self.__systems


    @property
    def systems_lock(self):
        '''returns the systems lock'''
        return self.__systems_lock


    @property
    def plugin_cfg(self):
        '''returns the plugin config [type name]'''
        return self.__plugin_cfg


    @property
    def plugin_cfg_lock(self):
        '''returns the plugin config lock'''
        return self.__plugin_cfg_lock


    @property
    def config(self):
        '''returns the value'''
        return self.__config


    @property
    def config_lock(self):
        '''returns the value'''
        return self.__config_lock


    @property
    def sql(self):
        '''returns the value'''
        return self.__sql


    @property
    def auth(self):
        '''returns the value'''
        return self.__auth


    @property
    def musicbrainz(self):
        '''returns the value'''
        return self.__musicbrainz
