from model.plex.PlexMediaItem import PlexMediaItem


class SourceService(object):
    def __init__(self, external_source, config, source_type):
        self.external_source = external_source
        self.config = config
        self.source_type = source_type

    def get_media_from_external_playlist(self, external_id):
        raise Exception("Method not implemented")

    def get_external_source(self):
        return self.external_source

    def get_config(self):
        return self.config

    def get_source_type(self):
        return self.source_type

    def set_external_source(self, external_source):
        self.external_source = external_source

    def set_config(self, config):
        self.config = config

    def set_source_type(self, source_type):
        self.source_type = source_type

    # TODO: See if we should put this somewhere else?
    def get_plex_media_items_from_external_id(self, plex_medias, external_id):
        items = []
        for plex_media in plex_medias:
            if plex_media.get_list_id() == external_id:
                items.append(plex_media)

        return items
