import enum


class ExternalSourceType(enum.Enum):
    IMDB = "imdb.com"
    TMDB = "tmdb.com"
    TVDB = "tvdb.com"
    TRAKT = "trakt.tv"