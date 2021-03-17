from plexapi.server import PlexServer
from model.external_source.enum.ExternalSourceType import ExternalSourceType
from model.plex.PlexGuid import PlexGuid
from model.plex.PlexMediaItem import PlexMediaItem

from plexapi.playlist import Playlist


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

    @staticmethod
    def parse_guid_id(guid):
        "imdb://tt0472043"

    # Checks if a given title with a given external id (e.g IMDB or TMDB id) exists within a playlist
    def get_plex_media(self, external_media):
        plex_service = self.get_connected_plex_service()
        movies = plex_service.library.section("Movies")
        tv_shows = plex_service.library.section("TV Shows")
        for movie in movies.search(external_media.get_media_name(), maxresults=10):
            # if movie.title == external_media.get_media_name():
            for guid in movie.guids:
                try:
                    plex_guid = PlexGuid.create_from_str(guid.id)

                    if plex_guid.get_source_type() == external_media.get_source_type():
                        if plex_guid.get_guid_id() == external_media.get_media_id():
                            return PlexMediaItem(
                                movie,
                                external_media.get_external_id(),
                                external_media.get_media_id(),
                            )
                except Exception as e:
                    print(str(e))

        """ 
        for tv_show in tv_shows.search(title):
            if tv_show.title == title:
                for guid in tv_show.guids:
                    if guid == ext_id:
                        return tv_show
        """
        return None

    def get_plex_media_objs_from_external_media_objs(self, external_medias):
        plex_media_objs = []
        for external_media in external_medias:
            plex_media = self.get_plex_media(external_media)
            if plex_media:
                plex_media_objs.append(plex_media)
            print("Finished search for: " + external_media.get_media_name())

        return plex_media_objs

    def delete_plex_playlist(self, plex_playlist):
        Playlist.delete(plex_playlist)

    def plex_playlist_exists(self, title):
        for playlist in self.get_connected_plex_service().playlists():
            if playlist.title == title:
                return True
        return False

    def fetch_plex_playlist_by_title(self, playlist_title):
        for playlist in self.get_connected_plex_service().playlists():
            if playlist.title == playlist_title:
                return playlist
        return None

    def create_playlist(self, title, items):
        Playlist.create(self.get_connected_plex_service(), title, items)
