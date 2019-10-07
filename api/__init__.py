'''ROOT API'''
import json
import cherrypy
from system.full import TackemSystemFull
from libs.root_event import RootEvent
from .base import APIBase
from .config import APIConfig


@cherrypy.expose
class API(APIBase):
    '''ROOT API'''


    def _cp_dispatch(self, vpath):
        '''cp dispatcher overwrite'''
        user = None
        if len(vpath) == 0:
            return self
        api_key = vpath.pop(0)
        user = self._check_api_key(api_key)
        if user == self.GUEST:
            user = self._check_session_id()
        cherrypy.request.params['user'] = user
        if len(vpath) == 0:
            return self

        section = vpath.pop(0)
        if section == "reboot":
            cherrypy.request.params['action'] = "reboot"
        elif section == "shutdown":
            cherrypy.request.params['action'] = "shutdown"
        elif section == "config":
            return APIConfig()
        # elif section == "":

        # elif section == "plugins":

        return self


    def GET(self, **kwargs):  # pylint: disable=invalid-name,no-self-use
        '''GET Function'''
        user = kwargs.get("user", self.GUEST)
        action = kwargs.get("action", None)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=401)  #Unauthorized
        if user == self.MASTER:
            if action == "shutdown":
                print("SHOULD SHUTDOWN")
                RootEvent.set_event("shutdown")
            elif action == "reboot":
                RootEvent.set_event("reboot")

        return json.dumps({
            "message" : "SUCCESS IN API KEY",
            "user" : user,
            "action": action
        })



#     @cherrypy.expose
#     def index(self, **kwargs):
#         '''First Run Will Load Into this page'''
#         cherrypy.response.headers['Content-Type'] = 'text/plain'
#         if not kwargs:
#             return "NO INPUT WHAT AM I TO DO?"

#         apikey = kwargs.get("key", False)
#         return_type = kwargs.get("return", "text")
#         plugin_name = kwargs.get("plugin", None)
#         system_name = kwargs.get("system", None)

#         if apikey is False:
#             return "NO API KEY"

#         apimode = self.__get_api_key(apikey)
#         if apimode is None:
#             return "API KEY INCORRECT"

#         if return_type not in ["text", "json", "html"]:
#             return "UKNOWN RETURN TYPE. CHOICES ARE: text json html"

#         plugin = None
#         system = None
#         single_instance_plugin = False

#         #Send to the config section
#         if system_name == "config":
#             return self.__config_api(kwargs, apimode)
#         #SEND TO A SYSTEM OR PLUGIN
#         if plugin_name is not None:
#             plugin = None
#             for plugin_type in self.__tackem_system.plugins():
#                 plugin = self.__tackem_system.plugin(plugin_type, plugin_name)
#                 if plugin is not None:
#                     break
#             if plugin is None:
#                 return "plugin " + plugin_name + " not found"
#             single_instance_plugin = plugin.SETTINGS['single_instance']
#         if single_instance_plugin:
#             if system_name is not None:
#                 system = self.__tackem_system.system(system_name)
#                 if system is None:
#                     return "system " + system_name + " not found"
#                 #TODO pass to the plugins api single mode
#                 return system_name + ": passing to system api"
#         else:
#             if system_name is not None and plugin_name is not None:
#                 system_full_name = plugin_name + system_name
#                 system = self.__tackem_system.system(system_full_name)
#                 if system is None:
#                     return "system not found"
#                 #TODO pass to the plugins api multi mode
#                 return plugin_name + " " + system_name + ": passing to system api"

#         #ROOT ACTIONS START HERE
#         action = kwargs.get("action", None)
#         if isinstance(action, str):
#             del kwargs["action"]
#             return action

#         return "Nothing Happened"
#     def __actions(self, action, kwargs=None):
#         '''all actions for the api here'''
#         if kwargs is None:
#             kwargs = {}
#         if action == "shutdown":
#             RootEvent.set_event("shutdown")
#         elif action == "reboot":
#             RootEvent.set_event("reboot")

#     def __config_api(self, kwargs, apimode):
#         '''section for the config api'''
#         json_set = kwargs.get("return", "text") == "json"
#         return_string = "IN THE CONFIG SECTION" + json.dumps(kwargs, ensure_ascii=False)

#         get = kwargs.get("get", False)
#         set_str = kwargs.get("set", False)
#         value = kwargs.get("value", False)

#         if isinstance(get, str):
#             return_string = self.__get_config_option(get, apimode)

#         if apimode and isinstance(set_str, str) and isinstance(value, str):
#             return_string = self.__set_config_option(get, value)

#         if json_set:
#             return json.dumps(return_string, ensure_ascii=False)
#         return str(return_string)
