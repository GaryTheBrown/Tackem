"""System to grab the info needed from the api for makemkv and the converter"""
from typing import Optional

from data.database.ripper import VIDEO_INFO_DB
from data.disc_type.base import DiscType
from data.disc_type.movie import MovieDiscType
from data.video_track_type.dontrip import DONTRIPTrackType
from data.video_track_type.extra import ExtraTrackType
from data.video_track_type.feature import FeatureTrackType
from data.video_track_type.trailer import TrailerTrackType
from libs.database import Database
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where


class DiscAPI:
    @classmethod
    def find_json(cls, uuid: str, label: str) -> str:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        info = None
        # if uuid == "36cc8c4d00000000" and label == "AQUA_TEEN_COLON_MOVIE":
        #     info = cls.__aqua_teen_movie().json()

        if info:
            Database.call(
                SQLUpdate(
                    VIDEO_INFO_DB,
                    Where("uuid", uuid),
                    Where("label", label),
                    rip_data=info.json(),
                    rip_data_download=True,
                )
            )
            return info.json()

        return "{}"

    @classmethod
    def find_disctype(cls, uuid: str, label: str) -> Optional[DiscType]:
        """will access the api and check if the disc exists
        TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO."""
        info = None
        # if uuid == "36cc8c4d00000000" and label == "AQUA_TEEN_COLON_MOVIE":
        #     return cls.__aqua_teen_movie()

        if info:
            Database.call(
                SQLUpdate(
                    VIDEO_INFO_DB,
                    Where("uuid", uuid),
                    Where("label", label),
                    rip_data=info.json(),
                    rip_data_download=True,
                )
            )
            return info

        return None

    @classmethod
    def __aqua_teen_movie(cls):
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

        return MovieDiscType("Aqua Teen Hunger Force Colon Movie", "", "2007", "tt0455326", tracks)
