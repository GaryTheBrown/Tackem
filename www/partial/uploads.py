"""Upload Partials"""
from libs.html_system import HTMLSystem


class PartialsUpload:
    """Upload Partials"""

    @classmethod
    def iso(cls):
        """returns a partial for iso upload"""
        return HTMLSystem.part("partial/uploads/iso")
