from model.config.PlexPlaylistItem import PlexPlaylistItem


class Config(object):
    def __init__(
        self, plex_api_token=None, plex_base_url=None, playlist_items=None
    ) -> None:
        self.plex_api_token = plex_api_token
        self.plex_base_url = plex_base_url
        self.playlist_items = playlist_items

    def get_plex_api_token(self):
        return self.plex_api_token

    def get_plex_base_url(self):
        return self.plex_base_url

    def get_playlist_items(self):
        return self.playlist_items

    def set_plex_api_token(self, plex_api_token):
        self.plex_api_token = plex_api_token

    def set_plex_base_url(self, plex_base_url):
        self.plex_base_url = plex_base_url

    def set_playlist_items(self, playlist_items):
        self.playlist_items = playlist_items
