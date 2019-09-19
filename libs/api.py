'''Script For the API Of The System'''
import json
import cherrypy
from libs.root_event import RootEvent
from system.full import TackemSystemFull

class API():
    '''API'''
    def __init__(self):
        self.__tackem_system = TackemSystemFull()

    def _get_api_key(self, key):
        '''checks the api key against the master and user keys and sets the correct modes
        True = Master
        False = User
        None = NONE'''
        if key == self.__tackem_system.get_config(["masterapi", "key"], None):
            return True
        elif key == self.__tackem_system.get_config(["userapi", "key"], None):
            return False
        return None

    @cherrypy.expose
    def index(self, **kwargs):
        '''First Run Will Load Into this page'''
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        if not kwargs:
            return "NO INPUT WHAT AM I TO DO?"

        apikey = kwargs.get("key", False)
        return_type = kwargs.get("return", "text")
        plugin_name = kwargs.get("plugin", None)
        system_name = kwargs.get("system", None)

        if apikey is False:
            return "NO API KEY"

        apimode = self._get_api_key(apikey)
        if apimode is None:
            return "API KEY INCORRECT"

        if return_type != "text" and return_type != "json" and return_type != "html":
            return "UKNOWN RETURN TYPE. CHOICES ARE: text json html"

        plugin = None
        system = None
        single_instance_plugin = False

        #Send to the config section
        if system_name == "config":
            return self._config_api(kwargs, apimode)
        #SEND TO A SYSTEM OR PLUGIN
        if plugin_name is not None:
            plugin = None
            for plugin_type in self.__tackem_system.plugins():
                plugin = self.__tackem_system.plugin(plugin_type, plugin_name)
                if plugin is not None:
                    break
            if plugin is None:
                return "plugin " + plugin_name + " not found"
            single_instance_plugin = plugin.SETTINGS['single_instance']
        if single_instance_plugin:
            if system_name is not None:
                system = self.__tackem_system.system(system_name)
                if system is None:
                    return "system " + system_name + " not found"
                #TODO pass to the plugins api single mode
                return system_name + ": passing to system api"
        else:
            if system_name is not None and plugin_name is not None:
                system_full_name = plugin_name + system_name
                system = self.__tackem_system.system(system_full_name)
                if system is None:
                    return "system not found"
                #TODO pass to the plugins api multi mode
                return plugin_name + " " + system_name + ": passing to system api"

        #ROOT ACTIONS START HERE
        action = kwargs.get("action", None)
        if isinstance(action, str):
            del kwargs["action"]
            return action

        return "Nothing Happened"

    def _actions(self, action, kwargs=None):
        '''all actions for the api here'''
        if kwargs is None:
            kwargs = {}
        if action == "shutdown":
            RootEvent().set_event("shutdown")
        elif action == "reboot":
            RootEvent().set_event("reboot")

    def _config_api(self, kwargs, apimode):
        '''section for the config api'''
        json_set = kwargs.get("return", "text") == "json"
        return_string = "IN THE CONFIG SECTION" + json.dumps(kwargs, ensure_ascii=False)

        get = kwargs.get("get", False)
        set_str = kwargs.get("set", False)
        value = kwargs.get("value", False)

        if isinstance(get, str):
            return_string = self._get_config_option(get, apimode)

        if apimode and isinstance(set_str, str) and isinstance(value, str):
            return_string = self._set_config_option(get, value)

        if json_set:
            return json.dumps(return_string, ensure_ascii=False)
        return str(return_string)

    def _get_config_option(self, get, apimode):
        '''the get config option api call'''
        if not apimode is True:
            if "api" in get:
                return "PERMISSION DENIED"
        data = get.split("/")
        val = self.__tackem_system.get_config(data, None)
        if val is None:
            return "ERROR"
        return val


    def _set_config_option(self, set_str, value):
        '''the get config option api call'''
        if not isinstance(value, str):
            return "ERROR NO VALUE GIVEN"
        data = set_str.split("/")
        return self.__tackem_system.set_config(data, value)
