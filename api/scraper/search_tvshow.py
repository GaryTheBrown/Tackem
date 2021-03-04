'''Search TV Show API'''
import cherrypy
from api.base import APIBase
from data.config import CONFIG

@cherrypy.expose
class APIScraperSearchTvshow(APIBase):
    '''Search TV Show API'''

    def POST(self, **kwargs) -> str:
        '''POST Function'''
        user = kwargs.get("user", self.GUEST)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=403)
        required = []
        if (plugin_type:= kwargs.get("plugin_type", "")) == "":
            required.append("plugin_type")
        if (plugin_name:= kwargs.get("plugin_name", "")) == "":
            required.append("plugin_name")
        if (instance:= kwargs.get("instance", "")) == "":
            required.append("instance")
        if required:
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Missing Data Passed. Requires {}".format(
                    ", ".join(required)),
                errorNumber=0
            )

        var = instance.lower().replace(" ", "")
        if var in CONFIG["plugins"][plugin_type][plugin_name].keys():
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Instance already exists",
                errorNumber=1
            )

        if not CONFIG["plugins"][plugin_type][plugin_name].clone_many_section(instance):
            return self._return_data(
                user,
                "addMulti",
                "Adding Instance of {} - {}".format(plugin_type, plugin_name),
                False,
                instance=instance,
                error="Cloning Data Failed",
                errorNumber=2
            )

        variable_name = "plugins_{}_{}".format(
            plugin_type, plugin_name)
        return self._return_data(
            user,
            "config",
            "Adding Instance of {} - {}".format(plugin_type, plugin_name),
            True,
            instance=instance,
            html=CONFIG["plugins"][plugin_type][plugin_name][instance].panel(
                variable_name,
                instance.title()
            )
        )

    # def searchtvshow(self, query: str, page: int = 1) -> str:
    #     '''search for a tv show'''
    #     return self.__search_for_tvshow(query, page)
