'''disc type information'''
import json
from . import video_track_type as track_type

class DiscType():
    '''Master Disc Type'''
    _types = ["movie", "tvshow"]
    def __init__(self, disc_type, tracks, language):
        if disc_type in self._types:
            self._disc_type = disc_type
        if isinstance(tracks, list):
            self._tracks = tracks
        if len(language) == 3 and isinstance(language, str):
            self._language = language

    def disc_type(self):
        '''returns the type'''
        return self._disc_type

    def tracks(self):
        '''returns the tracks'''
        return self._tracks

    def language(self):
        '''returns the discs main language'''
        return self._language

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["disc_type"] = self._disc_type
        if no_tracks:
            track_list = []
            for track in self._tracks:
                track_list.append(track.__dict__)
            super_dict["track_list"] = track_list
        return super_dict

class MovieDiscType(DiscType):
    '''Movie Disc Type'''
    def __init__(self, name, year, imdb_id, tracks, language="eng"):
        super().__init__("movie", tracks)
        self._name = name
        self._year = year
        self._imdb_id = imdb_id

    def name(self):
        '''returns movie name'''
        return self._name

    def year(self):
        '''returns movie year'''
        return self._year

    def imdb_id(self):
        '''returns movie imdb_id'''
        return self._imdb_id

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["year"] = self._year
        super_dict["imdb_id"] = self._imdb_id
        return super().make_dict(super_dict, no_tracks)

class TVShowDiscType(DiscType):
    '''TV Show Disc Type'''
    def __init__(self, name, tvdb_id, tracks, language="eng"):
        super().__init__("tvshow", tracks)
        self._name = name
        self._tvdb_id = tvdb_id

    def name(self):
        '''returns TV Show name'''
        return self._name

    def tvdb_id(self):
        '''returns TV Show name'''
        return self._tvdb_id

    def make_dict(self, super_dict=None, no_tracks=False):
        '''returns the tracks'''
        if super_dict is None:
            super_dict = {}
        super_dict["name"] = self._name
        super_dict["tvdb_id"] = self._tvdb_id
        return super().make_dict(super_dict, no_tracks)

def make_disc_type(data):
    '''transforms the data returned from the DB or API to the classes above'''
    if isinstance(data, str):
        data = json.loads(data)
    tracks = []
    for track in data['tracks']:
        if track['video_type'] == "dontrip":
            track.append(track_type.DONTRIPTrackType(track['reason']))
        elif track['video_type'] == "movie":
            track.append(track_type.MovieTrackType())
        elif track['video_type'] == "tvshow":
            track.append(track_type.TVShowTrackType(track['season_number'],
                                                    track['episode_number']))
        elif track['video_type'] == "trailer":
            track.append(track_type.TrailerTrackType(track['info']))
        elif track['video_type'] == "extra":
            track.append(track_type.ExtraTrackType(track['name']))
        elif track['video_type'] == "other":
            track.append(track_type.OtherTrackType(track['other_type']))

    if data['disc_type'] == "movie":
        return MovieDiscType(data['name'], data['year'], data['imdb_id'], tracks)
    if data['disc_type'] == "tvshow":
        return TVShowDiscType(data['name'], data['tvdb_id'], tracks)

    return data
