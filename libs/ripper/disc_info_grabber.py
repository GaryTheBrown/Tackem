'''function to grab the info needed for makemkv and the converter'''
import json
from data.database.ripper import VIDEO_INFO_DB_INFO as INFO_DB
from libs.database import Database
from libs.database.messages.insert import SQLInsert
from libs.database.messages.select import SQLSelect
from libs.database.messages.update import SQLUpdate
from libs.database.where import Where
from libs.ripper.data.disc_type import DiscType, make_disc_type
# from .data import disc_type, video_track_type as track_type


def grab_disc_info(uuid: str, label: str, sha256: str, disc_type: str) -> DiscType:
    '''checks the DB and API for the Disc info'''
    msg = SQLSelect(
        INFO_DB.name(),
        Where("uuid", uuid),
        Where("label", label),
        Where("sha256", sha256),
        Where("disc_type", disc_type),
    )
    Database.call(msg)

    if isinstance(msg.return_data, dict):
        Database.call(
            SQLUpdate(
                INFO_DB.name(),
                Where(
                    "id",
                    msg.return_data['id']
                ),
                ripped=False,
                ready_to_convert=False,
                ready_to_rename=False,
                ready_for_library=False,
                completed=False
            )
        )
    else:
        Database.call(
            SQLInsert(
                INFO_DB.name(),
                uuid=uuid,
                label=label,
                sha256=sha256,
                disc_type=disc_type,
                ripped=False,
                ready_to_convert=False,
                ready_to_rename=False,
                ready_for_library=False,
                completed=False
            )
        )

    Database.call(msg)

    rip_data_json = msg.return_data['rip_data']
    if rip_data_json is not None:
        return make_disc_type(json.loads(rip_data_json))

    rip_list = apiaccess_video_disc_id(uuid, label)
    if isinstance(rip_list, str):
        Database.call(
            SQLUpdate(
                INFO_DB.name(),
                Where("id", msg.return_data['id']),
                rip_data=rip_list
            )
        )
        return make_disc_type(json.loads(rip_list))




def apiaccess_video_disc_id(uuid: str, label: str):
    '''will access the api and check if the disc exists
    TEMP FUNCTION BELLOW TO EXPAND WHEN READY TO.'''
    return 1
    # uuid_temp = "36cc8c4d00000000"
    # label_temp = "AQUA_TEEN_COLON_MOVIE"
    # #when completing this function for real access make_disc_type is needed to be called
    # if uuid == uuid_temp and label == label_temp:
    #     tracks = [
    #         track_type.MovieTrackType(),
    #         track_type.DONTRIPTrackType("Blank"),
    #         track_type.DONTRIPTrackType("Legal Warning"),
    #         track_type.TrailerTrackType("Theatrical Trailer 4:3 version"),
    #         track_type.DONTRIPTrackType("Blank"),
    #         track_type.TrailerTrackType("Cahill Trailer (UnEarth)"),
    #         track_type.TrailerTrackType("Theatrical Trailer 16:9 version"),
    #         track_type.ExtraTrackType("Behind the scenes"),
    #         track_type.ExtraTrackType("Art/Music Gallery"),
    #         track_type.ExtraTrackType("Jon Schnep 3D"),
    #         track_type.DONTRIPTrackType("Legal Warning"),
    #         track_type.DONTRIPTrackType("Warner Brother Intro"),
    #         track_type.DONTRIPTrackType("Blank")
    #     ]

    #     return disc_type.MovieDiscType("Aqua Teen Hunger Force Colon Movie", "2007",
    #                                    "tt0455326", tracks)
