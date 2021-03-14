from plexapi.server import PlexServer
from model.external_source.enum.ExternalSourceType import ExternalSourceType


class PlexAPIService(object):
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token
        self.plex_service = None

    def get_base_url(self):
        return self.base_url

    def get_api_token(self):
        return self.api_token

    def get_connected_plex_service(self):
        if not self.plex_service:
            self.initiate_plex_service()
        return self.plex_service

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_api_token(self, api_token):
        self.api_token = api_token

    def set_plex_service(self, plex_service):
        self.plex_service = plex_service

    def initiate_plex_service(self):
        self.plex_service = PlexServer(self.base_url, self.api_token)

    # Checks if a given title with a given external id (e.g IMDB or TMDB id) exists within a playlist
    def media_exists(self, title, ext_id, ext_source_type):
        plex_service = self.get_connected_plex_service()
        movies = plex_service.library.section("Movies")
        for video in movies.search(title):
            if video.title == title:
                for guid in video.guids:
                    if guid == ext_id:
                        return True
        return False

    def media_exists_in_playlist(self, title, ext, playlist):
        pass
