"""Upload ISO API"""
import random
import string

import cherrypy

from api.base import APIBase
from data.database.post_upload import PostUpload


@cherrypy.expose
class APIRipperIsoUpload(APIBase):
    """Upload ISO API"""

    def POST(self, **kwargs) -> str:
        """POST Function"""

        if "filename" not in kwargs:
            return self._return_data(
                "Ripper",
                "Upload ISO",
                False,
                error="Missing Filename",
                errorNumber=0,
            )
        if "filesize" not in kwargs:
            return self._return_data(
                "Ripper",
                "Upload ISO",
                False,
                error="Missing Filesize",
                errorNumber=0,
            )

        existing = (
            PostUpload.do_select()
            .where(
                PostUpload.filename == kwargs["filename"], PostUpload.filesize == kwargs["filesize"]
            )
            .get()
        )
        url = cherrypy.url().split("/api/")[0]

        if existing:
            return self._return_data(
                "Ripper",
                "Upload ISO",
                True,
                key=existing.key,
                url=f"{url}/upload/?key={existing.key}",
            )

        rnd = random.SystemRandom()
        key = "".join(rnd.choices(string.ascii_lowercase + string.digits, k=40))
        upload = PostUpload()
        upload.key = key
        upload.filename = kwargs["filename"]
        upload.filesize = kwargs["filesize"]
        upload.system = "RIPPER_ISO"
        upload.save()

        return self._return_data(
            "Ripper",
            "Upload ISO",
            True,
            key=key,
            url=f"upload/{key}",
        )
