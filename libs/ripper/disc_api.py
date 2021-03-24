"""System to grab the info needed from the api for makemkv and the converter"""
from typing import Optional

from libs.ripper.data.disc_type import DiscType
from libs.ripper.data.disc_type import MovieDiscType
from libs.ripper.data.video_track_type import DONTRIPTrackType
from libs.ripper.data.video_track_type import ExtraTrackType
from libs.ripper.data.video_track_type import MovieTrackType
from libs.ripper.data.video_track_type import TrailerTrackType


class DiscAPI:
    @classmethod
    def find_json(cls, uuid: str, label: str) -> str:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        # if uuid == "36cc8c4d00000000" and label == "AQUA_TEEN_COLON_MOVIE":
        #     return cls.__aqua_teen_movie().json()

        return "{}"

    @classmethod
    def find_disctype(cls, uuid: str, label: str) -> Optional[DiscType]:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        # if uuid == "36cc8c4d00000000" and label == "AQUA_TEEN_COLON_MOVIE":
        #     return cls.__aqua_teen_movie()

        return None

    @classmethod
    def __aqua_teen_movie(cls):
        """TEMP RETURN OF THE DATA FOR Aqua Teen Hunger Force Colon Movie"""
        tracks = [
            MovieTrackType(),
            DONTRIPTrackType("Blank"),
            DONTRIPTrackType("Legal Warning"),
            TrailerTrackType("Theatrical Trailer 4:3 version"),
            DONTRIPTrackType("Blank"),
            TrailerTrackType("Cahill Trailer (UnEarth)"),
            TrailerTrackType("Theatrical Trailer 16:9 version"),
            ExtraTrackType("Behind the scenes"),
            ExtraTrackType("Art/Music Gallery"),
            ExtraTrackType("Jon Schnep 3D"),
            DONTRIPTrackType("Legal Warning"),
            DONTRIPTrackType("Warner Brother Intro"),
            DONTRIPTrackType("Blank"),
        ]

        return MovieDiscType("Aqua Teen Hunger Force Colon Movie", "", "2007", "tt0455326", tracks)
