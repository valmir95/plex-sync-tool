class ExternalSourceMedia(object):
    def __init__(self, media_name, media_id, source_type, external_id=None) -> None:
        self.media_name = media_name
        self.media_id = media_id
        self.source_type = source_type
        self.external_id = external_id

    def get_media_name(self):
        return self.media_name

    def get_media_id(self):
        return self.media_id

    def get_source_type(self):
        return self.source_type

    def get_external_id(self):
        return self.external_id

    def set_media_name(self, media_name):
        self.media_name = media_name

    def set_media_id(self, media_id):
        self.media_id = media_id

    def set_source_type(self, source_type):
        self.source_type = source_type

    def set_external_id(self, external_id):
        self.external_id = external_id
