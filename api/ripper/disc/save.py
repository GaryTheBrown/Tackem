"""Base Template For the API"""
import cherrypy

from api.base import APIBase


@cherrypy.expose
class APIRipperDiscSave(APIBase):
    """Base Template For the API"""

    def POST(self, disc_id: int, **kwargs):  # pylint: disable=invalid-name,no-self-use
        """POST Function"""

        data = {"tracks": []}
        for key, value in kwargs.items():
            if "_" not in key:
                continue
            if key == "disc_type":
                data["disc_type"] = value

            s = key.split("_")
            if s[0] == "disc":
                data[s[1]] = value
                continue

            if s[0] == "track":
                if int(s[1]) > len(data["tracks"]):
                    data["tracks"].append({s[2]: value})
                else:
                    data["tracks"][int(s[1]) - 1][s[2]] = value

        return self._return_data("Ripper", f"Save Disc - {disc_id}", True, lockable=True, data=data)
