'''System Data'''
import threading

class SystemData():
    '''System Data'''

    __plugins = {}  # [type][ name]
    __plugins_lock = threading.Lock()
    __systems = {}  # [type name]
    __systems_lock = threading.Lock()

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
    def systems(self):
        '''returns the systems [type name]'''
        with self.__systems_lock:
            return self.__systems

    @systems.setter
    def systems(self, systems):
        '''sets the systems'''
        with self.__systems_lock:
            self.__systems = systems
