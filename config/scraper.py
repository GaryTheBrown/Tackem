"""Scraper Config"""
from config.backend.list import ConfigList
from config.backend.obj.boolean import ConfigObjBoolean
from config.backend.obj.options.select import ConfigObjOptionsSelect
from config.backend.obj.string import ConfigObjString
from data.locale_options import OPTIONS as locale_options


def scraper_config() -> ConfigList:
    """Scraper Config"""
    return ConfigList(
        "scraper",
        "Video Scraper (The Movie DB)",
        ConfigObjString(
            "v4apikey",
            "",
            "V4 API Key",
            "The API key for TMDB API access goto http://www.themoviedb.org/ to grab your key",
        ),
        ConfigObjString(
            "url",
            "https://api.themoviedb.org",
            "Base Url",
            "The API base url for TMDB API access Leave alone unless you need to move this",
        ),
        ConfigObjBoolean("includeadult", False, "", "", hide_on_html=True),
        ConfigObjOptionsSelect(
            "language",
            locale_options,
            "en-gb",
            "Language",
            "language to use when scraping the data",
        ),
    )
