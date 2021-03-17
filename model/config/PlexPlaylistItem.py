class PlexPlaylistItem(object):
    def __init__(self, playlist_name=None, external_list_source=None, external_list_ids=None, exact_sync=None) -> None:
        self.playlist_name = playlist_name
        self.external_list_source = external_list_source
        self.external_list_ids = external_list_ids
        self.exact_sync = exact_sync

    def get_playlist_name(self):
        return self.playlist_name

    def get_external_list_source(self):
        return self.external_list_source

    def get_external_list_ids(self):
        return self.external_list_ids

    def get_exact_sync(self):
        return self.exact_sync

    def set_playlist_name(self, playlist_name):
        self.playlist_name = playlist_name

    def set_external_list_source(self, external_list_source):
        self.external_list_source = external_list_source

    def set_external_list_ids(self, external_list_ids):
        self.external_list_ids = external_list_ids

    def set_exact_sync(self, exact_sync):
        self.exact_sync = exact_sync