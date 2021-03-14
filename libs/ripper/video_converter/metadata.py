'''Video Controller MetaData code'''
from libs.ripper.data.disc_type import DiscType
from libs.ripper.data.video_track_type import VideoTrackType
from libs.scraper import Scraper
from libs.ripper.video_converter.base import VideoConverterBase


class VideoConverterMetadata(VideoConverterBase):
    '''Video Controller MetaData code'''

    def _sort_metadata(self, disc_info: DiscType, track_info: VideoTrackType):
        '''sorts out the metadata'''
        if self._conf['video']['videoinserttags'].value is False:
            return

        disc_type = disc_info.disc_type
        track_type = track_info.video_type
        tags = []
        scraper_data = None
        if disc_type == "Movie":
            scraper_info = Scraper.get_movie_details(disc_info.moviedbid)
            if scraper_info['success']:
                scraper_data = scraper_info['response']
            if track_type == "movie":
                tags.append('title="' + disc_info.name + '"')
                tags.append('year=' + str(disc_info.year))
            elif track_type == "extra":
                extra_title = disc_info.name + " (" + str(disc_info.year)
                extra_title += ") - " + track_info.name
                tags.append('title="' + extra_title + '"')
            elif track_type == "trailer":
                trailer_title = disc_info.name + " (" + str(disc_info.year())
                trailer_title += ") - " + track_info.info
                tags.append('title="' + trailer_title + '"')
            elif track_type == "other":
                other_title = disc_info.name
                other_title += ") - " + track_info.other_type
                tags.append('title="' + other_title + '"')
        elif disc_type == "TV Show":
            tags.append('show="' + disc_info.name + '"')
            if track_type == "tvshow":
                scraper_info = Scraper.get_tvshow_episode_details(disc_info.moviedbid,
                                                                  track_info.season,
                                                                  track_info.episode)
                scraper_data = scraper_info['response']
                tags.append('season=' + str(track_info.season))
                tags.append('episode=' + str(track_info.episode))
                tags.append('title="' + scraper_data['name'] + '"')
            elif track_type == "extra":
                tags.append('title="' + track_info.name + '"')
            elif track_type == "trailer":
                tags.append('title="' + track_info.info + '"')
            elif track_type == "other":
                tags.append(
                    'title="' + track_info.other_type + '"')
        tags.append('language="' + disc_info.language + '"')

        for tag in tags:
            self._command.append('-metadata')
            self._command.append(tag)
