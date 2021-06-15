from plexapi.server import PlexServer
from model.external_source.enum.ExternalSourceType import ExternalSourceType
from model.plex.PlexGuid import PlexGuid
from model.plex.PlexMediaItem import PlexMediaItem
from model.plex.enum.ComparatorStrategy import ComparatorStrategy
from model.shared.enum.MediaType import MediaType

from plexapi.playlist import Playlist


class PlexAPIService(object):
    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.api_token = api_token
        self.plex_service = self.initiate_plex_service()

    def get_base_url(self):
        return self.base_url

    def get_api_token(self):
        return self.api_token

    def get_connected_plex_service(self):
        if not self.plex_service:
            return self.initiate_plex_service()
        return self.plex_service

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_api_token(self, api_token):
        self.api_token = api_token

    def set_plex_service(self, plex_service):
        self.plex_service = plex_service

    def initiate_plex_service(self):
        try:
            plex_service = PlexServer(self.base_url, self.api_token)
            # As stupid as this may seem, this is seems to be the only way to "ping" the server and check if it works
            plex_service.playlists()
            return plex_service
        except:
            raise Exception("Could not connect to Plex. Check your base url and/or plex token.")

    def get_plex_media(self, external_media, comparator_strategy):
        section = self.get_plex_section_by_media_type(external_media.get_media_type())
        for media in section.search(external_media.get_media_name(), maxresults=None):
            match = comparator_strategy.compare_external_and_plex_media(external_media, media)
            if match:
                return match
        return None

    def get_plex_media_objs_from_external_media_objs(self, external_medias, comparator_strategy):
        plex_media_objs = []
        for external_media in external_medias:
            plex_media = self.get_plex_media(external_media, comparator_strategy)
            if plex_media:
                plex_media_objs.append(plex_media)
            else:
                print("Found no match for " + external_media.get_media_name())
            print("Finished search for: " + external_media.get_media_name())

        return plex_media_objs

    def delete_plex_playlist(self, plex_playlist):
        Playlist.delete(plex_playlist)

    def get_plex_section_by_media_type(self, external_media_type):
        plex_service = self.get_connected_plex_service()
        if external_media_type == MediaType.MOVIE:
            return plex_service.library.section("Movies")
        elif external_media_type == MediaType.TV:
            return plex_service.library.section("TV Shows")

        raise Exception("Media has no supported media type")

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
