"""disc type information"""
from typing import List
from typing import Optional

from config.backend.obj.data.input_attributes import InputAttributes
from config.backend.obj.data.option import ConfigObjOption
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from data.disc_type.base import DiscType
from data.languages import Languages


class HomeMovieDiscType(DiscType):
    """HomeMovie Disc Type"""

    _track_types: List[str] = ["Dont Rip", "Home Movie"]

    def __init__(self, name: str, info: str, tracks: list, language: str = "eng"):
        super().__init__("Home Movie", name, tracks, language, None)
        self.__info = info

    @property
    def info(self) -> str:
        """returns the temp info"""
        return self.__info

    def make_dict(self, super_dict: Optional[dict] = None, no_tracks: bool = False) -> dict:
        """returns the tracks"""
        if super_dict is None:
            super_dict = {}
        super_dict["info"] = self.info
        return DiscType.make_dict(self, super_dict, no_tracks)

    def track_title(self, index: int):
        """generates the title for the track"""
        return f"Home Movie {self.name.capitalize()} - {self.tracks[index].title}"

    def html_create_data(self, read_only: bool = False) -> dict:
        """returns the data for html"""
        name = ConfigObjString(
            "disc_name",
            "",
            "Disc Name",
            "Enter the name of the Disc here",
        )
        name.value = self.name
        if read_only:
            name.input_attributes = InputAttributes("readonly")

        info = ConfigObjString(
            "disc_info",
            "",
            "Disc Info",
            "Enter some information for the disc here",
        )
        info.value = self.info
        if read_only:
            info.input_attributes = InputAttributes("readonly")

        language = ConfigObjOptionsSelect(
            "disc_language",
            Languages.config_option_2(ConfigObjOption),
            "en",
            "Disc Language",
            "Enter the language of the Disc here",
        )
        language.value = self.language
        if read_only:
            language.input_attributes = InputAttributes("readonly")

        return {
            "search": False,
            "disc_type": self.disc_type,
            "disc_items": [
                {
                    "type": "hidden",
                    "var_name": "disc_type",
                    "value": self.disc_type,
                },
                name.html_dict(""),
                info.html_dict(""),
                language.html_dict(""),
            ],
        }

    def html_show_data(self, read_only: bool = False) -> dict:
        """returns the data for html"""
        return {"tracks": [x.html_create_data(i + 1, read_only) for i, x in enumerate(self.tracks)]}
