"""Upload Video ISO API"""
import random
import string

import cherrypy

from api.base import APIBase
from data.database.system import UPLOAD_DB
from libs.database import Database
from libs.database.messages import SQLInsert
from libs.database.messages import SQLSelect
from libs.database.where import Where


@cherrypy.expose
class APIRipperIsoUploadVideo(APIBase):
    """Upload Video ISO API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""
        user = kwargs.get("user", self.GUEST)
        if user == self.GUEST:
            raise cherrypy.HTTPError(status=403)

        if "filename" not in kwargs:
            return self._return_data(
                user,
                "Ripper",
                "Upload Video ISO",
                False,
                error="Missing Filename",
                errorNumber=1,
            )
        if "filesize" not in kwargs:
            return self._return_data(
                user,
                "Ripper",
                "Upload Video ISO",
                False,
                error="Missing Filesize",
                errorNumber=2,
            )

        msg = SQLSelect(
            UPLOAD_DB,
            Where("filename", kwargs["filename"]),
            Where("filesize", kwargs["filesize"]),
        )

        Database.call(msg)
        url = cherrypy.url().split("/api/")[0]
        if isinstance(msg.return_data, dict):
            return self._return_data(
                user,
                "Ripper",
                "Upload Video ISO",
                True,
                url=f"{url}/upload/?key={msg.return_data['key']}",
            )

        rnd = random.SystemRandom()
        key = "".join(rnd.choices(string.ascii_lowercase + string.digits, k=40))
        Database.call(
            SQLInsert(
                UPLOAD_DB,
                key=key,
                filename=kwargs["filename"],
                filesize=kwargs["filesize"],
                system="RIPPER_ISO_VIDEO",
            )
        )

        return self._return_data(
            user, "Ripper", "Upload Video ISO", True, url=f"{url}/upload/?key={key}"
        )
