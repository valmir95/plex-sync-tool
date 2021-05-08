class PlexPlaylistItem(object):
    def __init__(self, playlist_name=None, external_list_urls=None, exact_sync=None) -> None:
        self.playlist_name = playlist_name
        self.external_list_urls = external_list_urls
        self.exact_sync = exact_sync

    def get_playlist_name(self):
        return self.playlist_name

    def get_external_list_urls(self):
        return self.external_list_urls

    def get_exact_sync(self):
        return self.exact_sync

    def set_playlist_name(self, playlist_name):
        self.playlist_name = playlist_name

    def set_external_list_urls(self, external_list_urls):
        self.external_list_urls = external_list_urls

    def set_exact_sync(self, exact_sync):
        self.exact_sync = exact_sync