'''System Data'''
import threading


class SystemData():
    '''System Data'''


    __plugins = {} # [type][ name]
    __plugins_lock = threading.Lock()
    __systems = {} # [type name]
    __systems_lock = threading.Lock()
    __config = None
    __config_lock = threading.Lock()
    __sql = None
    __auth = None
    __musicbrainz = None


    @property
    def plugins(self):
        '''returns the plugin [type][ name]'''
        with self.__plugins_lock:
            return self.__plugins


    @plugins.setter
    def plugins(self, plugins):
        '''sets the plugins'''
        with self.__plugins_lock:
            self.__plugins = plugins


    @property
    def plugins_lock(self):
        '''returns the plugins_lock'''
        return self.__plugins_lock


    @property
    def systems(self):
        '''returns the systems [type name]'''
        with self.__systems_lock:
            return self.__systems


    @systems.setter
    def systems(self, systems):
        '''sets the systems'''
        with self.__systems_lock:
            self.__systems = systems


    @property
    def systems_lock(self):
        '''returns the systems lock'''
        return self.__systems_lock


    @property
    def config(self):
        '''returns the value'''
        with self.__config_lock:
            return self.__config


    @config.setter
    def config(self, config):
        '''sets the config file'''
        with self.__config_lock:
            self.__config = config


    @property
    def config_lock(self):
        '''returns the value'''
        return self.__config_lock


    @property
    def sql(self):
        '''returns the value'''
        return self.__sql


    @sql.setter
    def sql(self, sql):
        '''returns the value'''
        self.__sql = sql


    @property
    def auth(self):
        '''returns the value'''
        return self.__auth


    @auth.setter
    def auth(self, auth):
        '''returns the value'''
        self.__auth = auth


    @property
    def musicbrainz(self):
        '''returns the value'''
        return self.__musicbrainz


    @musicbrainz.setter
    def musicbrainz(self, musicbrainz):
        '''returns the value'''
        self.__musicbrainz = musicbrainz
