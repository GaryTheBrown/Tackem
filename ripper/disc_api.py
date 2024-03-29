"""System to grab the info needed from the api for makemkv and the converter"""
from typing import Optional

from data.disc_type.base import DiscType
from data.disc_type.movie import MovieDiscType
from data.video_track_type.dontrip import DONTRIPTrackType
from data.video_track_type.extra import ExtraTrackType
from data.video_track_type.feature import FeatureTrackType
from data.video_track_type.trailer import TrailerTrackType


class DiscAPI:
    @classmethod
    def find_json(cls, uuid: str, label: str) -> str:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        info = cls.find_disctype(uuid, label)
        return info.json() if info else "{}"

    @classmethod
    def find_disctype(cls, uuid: str, label: str) -> Optional[DiscType]:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        info = None
        # if uuid == "36cc8c4d00000000" and label == "AQUA_TEEN_COLON_MOVIE":
        #     return cls.__aqua_teen_movie()
        return info

    @staticmethod
    def __aqua_teen_movie():
        """TEMP RETURN OF THE DATA FOR Aqua Teen Hunger Force Colon Movie"""
        tracks = [
            FeatureTrackType(),
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

        return MovieDiscType("Aqua Teen Hunger Force Colon Movie", "", 2007, 275, tracks)
