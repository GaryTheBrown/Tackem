"""Template for dealing with the template system"""
import os
import types

import cherrypy
import jinja2

from data.config import CONFIG
from libs.authentication import Authentication
from libs.ripper import Ripper


class Template(cherrypy.Tool):
    """Template for dealing with the template system"""

    _engine = None
    """Jinja environment instance"""
    _baseurl: str = None

    def __init__(self):
        viewLoader = jinja2.FileSystemLoader(os.path.join(os.getcwd(), "www", "view"))
        self._engine = jinja2.Environment(
            loader=viewLoader,
            autoescape=True,
            cache_size=0,
            auto_reload=True,
            extensions=["jinja2.ext.loopcontrols"],
        )
        if self._baseurl is None:
            self._baseurl = CONFIG["webui"]["baseurl"].value

        cherrypy.Tool.__init__(self, "before_handler", self.render)

    def __call__(self, *args, **kwargs):
        # Add in Globals here

        if args and isinstance(args[0], (types.FunctionType, types.MethodType)):
            # @template
            args[0].exposed = True
            return cherrypy.Tool.__call__(self, **kwargs)(args[0])
        else:
            # @template()
            def wrap(f):
                f.exposed = True
                return cherrypy.Tool.__call__(self, *args, **kwargs)(f)

            return wrap

    def render(self, user: int = Authentication.GUEST):

        handler = cherrypy.serving.request.handler

        def wrap(*args, **kwargs):

            return self._render(user, handler, *args, **kwargs)

        cherrypy.serving.request.handler = wrap

    def _render(self, user, handler, *args, **kwargs):

        parts = []
        if hasattr(handler.callable, "__self__"):
            parts.append(handler.callable.__self__.__class__.__name__.lower())
        if hasattr(handler.callable, "__name__"):
            parts.append(handler.callable.__name__.lower())
        template = "/".join(parts)
        data = handler(*args, **kwargs) or {}

        data.update(self.__global_vars(data))
        if user > Authentication.GUEST:
            Authentication.check_auth()
        if user == Authentication.ADMIN:
            Authentication.is_admin()
        renderer = self._engine.get_template(f"page/{template}.html")
        data["loggedin"] = Authentication.check_logged_in() > 0
        data["isadmin"] = Authentication.check_logged_in() == 2

        return renderer.render(**data) if template and isinstance(data, dict) else data

    def __global_vars(self, kwargs) -> dict:
        """generates the globally needed variables here"""

        return_dict = {
            "baseurl": self._baseurl,
            "loggedin": kwargs.get("loggedin", False),
            "isadmin": kwargs.get("isadmin", False),
            "navbar": {"ripper": Ripper.enabled},
        }
        return return_dict
