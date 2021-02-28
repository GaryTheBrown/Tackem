'''function to grab the info needed for makemkv and the converter'''
import json
from subprocess import DEVNULL, PIPE, Popen
from data.database.ripper import VIDEO_INFO_DB
from libs.database import Database
from libs.database.messages import SQLInsert
from libs.database.messages import SQLSelect
from libs.database.messages import SQLUpdate
from libs.database.where import Where
from libs.ripper.data.disc_type import DiscType, make_disc_type
# from .data import disc_type, video_track_type as track_type

def rip_data(db_data: dict) -> DiscType:
    '''comment'''
    if db_data['rip_data'] is not None:
        return make_disc_type(json.loads(db_data['rip_data']))

    rip_list = apiaccess_video_disc_id(db_data['uuid'], db_data['label'])
    if isinstance(rip_list, str) and isinstance(json.loads(rip_list), (dict, list)):
        Database.call(
            SQLUpdate(
                VIDEO_INFO_DB,
                Where("id", db_data['id']),
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

def gen_sha256_linux(in_file: str) -> str:
    '''Generates the sha256'''
    # using DD to read the disc pass it to sha256 to make a unique code for searching by
    dd_process = Popen(["dd", "if=" + in_file, "bs=4M", "count=128", "status=none"],
                        stdout=PIPE, stderr=DEVNULL)
    sha256sum = Popen(["sha256sum"], stdin=dd_process.stdout, stdout=PIPE, stderr=DEVNULL)
    if dd_process.returncode == 0:
        return sha256sum.communicate()[0].decode('utf-8').replace("-", "").rstrip()
    return ""
